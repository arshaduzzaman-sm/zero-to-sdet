"""The database tables. The diagram is in practice-app/DESIGN.md section 4.

Money is whole cents (1299 means 12.99). Times are UTC.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    full_name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="customer")
    is_verified: Mapped[bool] = mapped_column(default=False)
    failed_logins: Mapped[int] = mapped_column(default=0)
    locked_until: Mapped[datetime | None]
    shipping_address: Mapped[str | None] = mapped_column(String(300))
    created_at: Mapped[datetime]


class OtpCode(Base):
    __tablename__ = "otp_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    code_hash: Mapped[str] = mapped_column(String(64))
    purpose: Mapped[str] = mapped_column(String(10))  # "verify" or "reset"
    attempts: Mapped[int] = mapped_column(default=0)
    expires_at: Mapped[datetime]
    used_at: Mapped[datetime | None]
    created_at: Mapped[datetime]


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    slug: Mapped[str] = mapped_column(String(60), unique=True)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, default="")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    price_cents: Mapped[int]
    stock: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)
    image_path: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime]

    category: Mapped[Category] = relationship(lazy="joined")


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    coupon_code: Mapped[str | None] = mapped_column(String(32))
    updated_at: Mapped[datetime]

    items: Mapped[list[CartItem]] = relationship(
        lazy="selectin", cascade="all, delete-orphan", order_by="CartItem.product_id"
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int]

    product: Mapped[Product] = relationship(lazy="joined")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), index=True)
    subtotal_cents: Mapped[int]
    discount_cents: Mapped[int]
    tax_cents: Mapped[int]
    shipping_cents: Mapped[int]
    total_cents: Mapped[int]
    coupon_code: Mapped[str | None] = mapped_column(String(32))
    shipping_address: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    items: Mapped[list[OrderItem]] = relationship(
        lazy="selectin", cascade="all, delete-orphan", order_by="OrderItem.product_id"
    )
    payments: Mapped[list[Payment]] = relationship(lazy="selectin", order_by="Payment.id")
    user: Mapped[User] = relationship(lazy="joined")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int]
    unit_price_cents: Mapped[int]

    product: Mapped[Product] = relationship(lazy="joined")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    card_last4: Mapped[str] = mapped_column(String(4))
    status: Mapped[str] = mapped_column(String(20))  # succeeded, declined, timeout, refunded
    amount_cents: Mapped[int]
    sandbox_ref: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime]


class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    kind: Mapped[str] = mapped_column(String(20))  # "percent" or "free_shipping"
    value: Mapped[int] = mapped_column(default=0)  # percent off, for "percent"
    ends_at: Mapped[datetime]
    once_per_customer: Mapped[bool] = mapped_column(default=False)


class CouponUse(Base):
    __tablename__ = "coupon_uses"

    id: Mapped[int] = mapped_column(primary_key=True)
    coupon_id: Mapped[int] = mapped_column(ForeignKey("coupons.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)


class File(Base):
    """Uploaded and generated files (used from step 1.5.5)."""

    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))  # avatar, product_image, invoice
    original_name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int]
    storage_path: Mapped[str] = mapped_column(String(255))
    sha256: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime]


class Review(Base):
    """Product reviews. With Docker they live in MongoDB (step 1.5.3); without Docker
    (SQLite mode) they live in this table."""

    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint("product_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    username: Mapped[str] = mapped_column(String(20))
    rating: Mapped[int]
    text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime]
