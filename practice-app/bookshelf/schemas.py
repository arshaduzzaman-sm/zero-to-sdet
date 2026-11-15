"""What the API accepts and returns. These models also build the /docs page."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME = r"^[A-Za-z0-9_]{3,20}$"


def clean_email(value: str) -> str:
    value = value.strip().lower()
    if len(value) > 254 or not EMAIL.match(value):
        raise ValueError("Enter a valid email address, like name@example.com.")
    return value


def strong_password(value: str) -> str:
    if not (any(c.isalpha() for c in value) and any(c.isdigit() for c in value)):
        raise ValueError("Use at least one letter and one digit.")
    return value


class Message(BaseModel):
    message: str


# ----- Accounts -----


class SignupIn(BaseModel):
    email: str = Field(examples=["new.tester@example.com"])
    username: str = Field(pattern=USERNAME, examples=["new_tester"])
    full_name: str = Field(min_length=1, max_length=100, examples=["New Tester"])
    password: str = Field(min_length=8, max_length=128, examples=["Test@1234"])

    _email = field_validator("email")(clean_email)
    _password = field_validator("password")(strong_password)

    @field_validator("username")
    @classmethod
    def _lower(cls, value: str) -> str:
        return value.lower()

    @field_validator("full_name")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Enter your name.")
        return value.strip()


class EmailIn(BaseModel):
    email: str = Field(examples=["arshad@example.com"])
    _email = field_validator("email")(clean_email)


class VerifyIn(EmailIn):
    code: str = Field(pattern=r"^\d{6}$", examples=["123456"])


class ResetPasswordIn(VerifyIn):
    new_password: str = Field(min_length=8, max_length=128)
    _password = field_validator("new_password")(strong_password)


class LoginIn(BaseModel):
    username: str = Field(
        min_length=1, max_length=254, description="Username or email", examples=["arshad"]
    )
    password: str = Field(min_length=1, max_length=128, examples=["Test@1234"])


class TokenOut(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"  # noqa: S105  (the word "bearer", not a secret)
    expires_in: int = Field(description="Seconds until the token stops working")


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_verified: bool
    shipping_address: str | None
    created_at: datetime


class UserUpdateIn(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    shipping_address: str | None = Field(default=None, max_length=300)


# ----- Catalog -----


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str


class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    description: str
    category: CategoryOut
    price_cents: int
    stock: int
    in_stock: bool
    is_active: bool
    rating_average: float | None
    rating_count: int
    created_at: datetime


class ProductIn(BaseModel):
    sku: str = Field(pattern=r"^[A-Z0-9-]{3,32}$", examples=["BK-NEW-001"])
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)
    category_id: int
    price_cents: int = Field(gt=0, le=1_000_000)
    stock: int = Field(ge=0, le=100_000)
    is_active: bool = True


class ProductUpdateIn(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    category_id: int | None = None
    price_cents: int | None = Field(default=None, gt=0, le=1_000_000)
    stock: int | None = Field(default=None, ge=0, le=100_000)
    is_active: bool | None = None


class ReviewIn(BaseModel):
    rating: int = Field(ge=1, le=5)
    text: str = Field(min_length=1, max_length=500)

    @field_validator("text")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Write a few words.")
        return value.strip()


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    user_id: int
    username: str
    rating: int
    text: str
    created_at: datetime


class Page[T](BaseModel):
    items: list[T]
    page: int
    size: int
    total: int
    pages: int


# ----- Cart, checkout, orders -----


class CartItemIn(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, le=10)


class QuantityIn(BaseModel):
    quantity: int = Field(ge=1, le=10)


class CouponIn(BaseModel):
    code: str = Field(min_length=1, max_length=32, examples=["WELCOME10"])


class CartLineOut(BaseModel):
    product_id: int
    sku: str
    name: str
    unit_price_cents: int
    quantity: int
    line_total_cents: int
    available: bool


class CartOut(BaseModel):
    items: list[CartLineOut]
    item_count: int
    coupon_code: str | None
    subtotal_cents: int
    discount_cents: int
    tax_cents: int
    shipping_cents: int
    total_cents: int


class CheckoutIn(BaseModel):
    shipping_address: str | None = Field(
        default=None, max_length=300, description="Leave out to use the address in your profile"
    )
    card_number: str = Field(
        min_length=12,
        max_length=23,
        description="Sandbox cards only: 4242 4242 4242 4242 succeeds, "
        "4000 0000 0000 0002 is declined, 4000 0000 0000 9995 times out",
        examples=["4242 4242 4242 4242"],
    )
    expiry: str = Field(pattern=r"^(0[1-9]|1[0-2])/\d{2}$", examples=["12/30"])
    cvc: str = Field(pattern=r"^\d{3}$", examples=["123"])


class OrderLineOut(BaseModel):
    product_id: int
    sku: str
    name: str
    quantity: int
    unit_price_cents: int
    line_total_cents: int


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    card_last4: str
    amount_cents: int
    sandbox_ref: str
    created_at: datetime


class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    items: list[OrderLineOut]
    coupon_code: str | None
    subtotal_cents: int
    discount_cents: int
    tax_cents: int
    shipping_cents: int
    total_cents: int
    shipping_address: str
    payments: list[PaymentOut]
    created_at: datetime
    updated_at: datetime


class OrderStatusIn(BaseModel):
    status: Literal["shipped", "delivered"]


class ClockIn(BaseModel):
    now: datetime | None = Field(default=None, description="Set the app's 'now' (ISO 8601)")
    advance_seconds: int | None = Field(
        default=None, ge=1, le=10 * 365 * 24 * 3600, description="Move the clock forward"
    )


class ClockOut(BaseModel):
    now: datetime
    is_real_time: bool
