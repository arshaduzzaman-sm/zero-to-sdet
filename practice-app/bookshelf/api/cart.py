"""The shopping cart: add, change, remove, coupons, totals."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import money
from ..deps import AppClock, CurrentUser, Db
from ..errors import ApiError
from ..models import Cart, CartItem, Coupon, CouponUse, Product, User
from ..schemas import CartItemIn, CartLineOut, CartOut, CouponIn, QuantityIn

router = APIRouter(prefix="/cart", tags=["Cart"])

MAX_QUANTITY = 10


def get_cart(db: Session, user: User, now: datetime) -> Cart:
    cart = db.scalars(select(Cart).where(Cart.user_id == user.id)).first()
    if cart is None:
        cart = Cart(user_id=user.id, updated_at=now)
        db.add(cart)
        db.flush()
    return cart


def find_coupon(db: Session, code: str) -> Coupon | None:
    return db.scalars(select(Coupon).where(Coupon.code == code.strip().upper())).first()


def check_coupon(db: Session, coupon: Coupon | None, user: User, now: datetime) -> Coupon:
    if coupon is None:
        raise ApiError(404, "COUPON_NOT_FOUND", "There is no coupon with that code.")
    if coupon.ends_at <= now:
        raise ApiError(400, "COUPON_EXPIRED", f"The coupon {coupon.code} has ended.")
    if (
        coupon.once_per_customer
        and db.scalars(
            select(CouponUse).where(CouponUse.coupon_id == coupon.id, CouponUse.user_id == user.id)
        ).first()
    ):
        raise ApiError(400, "COUPON_ALREADY_USED", f"You have already used {coupon.code}.")
    return coupon


def cart_totals(db: Session, cart: Cart) -> money.Totals:
    subtotal = sum(
        item.product.price_cents * item.quantity for item in cart.items if item.product.is_active
    )
    coupon = find_coupon(db, cart.coupon_code) if cart.coupon_code else None
    if coupon is None:
        return money.calculate(subtotal)
    return money.calculate(subtotal, coupon.kind, coupon.value)


def cart_out(db: Session, cart: Cart) -> CartOut:
    lines = [
        CartLineOut(
            product_id=item.product_id,
            sku=item.product.sku,
            name=item.product.name,
            unit_price_cents=item.product.price_cents,
            quantity=item.quantity,
            line_total_cents=item.product.price_cents * item.quantity,
            available=item.product.is_active and item.product.stock >= item.quantity,
        )
        for item in cart.items
    ]
    return CartOut(
        items=lines,
        item_count=sum(line.quantity for line in lines),
        coupon_code=cart.coupon_code,
        **cart_totals(db, cart).as_dict(),
    )


def check_quantity(product: Product, quantity: int) -> None:
    if quantity > MAX_QUANTITY:
        raise ApiError(400, "QUANTITY_LIMIT", f"You can buy at most {MAX_QUANTITY} of one product.")
    if quantity > product.stock:
        left = "none are" if product.stock == 0 else f"only {product.stock} are"
        raise ApiError(
            409,
            "OUT_OF_STOCK",
            f"Sorry, {left} left of {product.name}.",
            details={"product_id": product.id, "stock": product.stock},
        )


def find_item(cart: Cart, product_id: int) -> CartItem:
    for item in cart.items:
        if item.product_id == product_id:
            return item
    raise ApiError(404, "ITEM_NOT_IN_CART", "That product is not in your cart.")


@router.get("", response_model=CartOut, summary="See my cart and its totals")
def show_cart(user: CurrentUser, db: Db, clock: AppClock) -> CartOut:
    cart = get_cart(db, user, clock.now())
    db.commit()
    return cart_out(db, cart)


@router.post("/items", response_model=CartOut, summary="Add a product to my cart")
def add_item(body: CartItemIn, user: CurrentUser, db: Db, clock: AppClock) -> CartOut:
    """Adding a product that is already in the cart adds to its quantity."""
    product = db.get(Product, body.product_id)
    if product is None or not product.is_active:
        raise ApiError(404, "PRODUCT_NOT_FOUND", "Product not found.")
    now = clock.now()
    cart = get_cart(db, user, now)
    existing = next((i for i in cart.items if i.product_id == product.id), None)
    quantity = body.quantity + (existing.quantity if existing else 0)
    check_quantity(product, quantity)
    if existing:
        existing.quantity = quantity
    else:
        cart.items.append(CartItem(product_id=product.id, quantity=quantity, product=product))
    cart.updated_at = now
    db.commit()
    return cart_out(db, cart)


@router.patch("/items/{product_id}", response_model=CartOut, summary="Change a quantity")
def change_quantity(
    product_id: int, body: QuantityIn, user: CurrentUser, db: Db, clock: AppClock
) -> CartOut:
    now = clock.now()
    cart = get_cart(db, user, now)
    item = find_item(cart, product_id)
    check_quantity(item.product, body.quantity)
    item.quantity = body.quantity
    cart.updated_at = now
    db.commit()
    return cart_out(db, cart)


@router.delete("/items/{product_id}", response_model=CartOut, summary="Remove a product")
def remove_item(product_id: int, user: CurrentUser, db: Db, clock: AppClock) -> CartOut:
    now = clock.now()
    cart = get_cart(db, user, now)
    cart.items.remove(find_item(cart, product_id))
    cart.updated_at = now
    db.commit()
    return cart_out(db, cart)


@router.post("/coupon", response_model=CartOut, summary="Use a coupon code")
def apply_coupon(body: CouponIn, user: CurrentUser, db: Db, clock: AppClock) -> CartOut:
    """One coupon per cart. A new code replaces the old one."""
    now = clock.now()
    coupon = check_coupon(db, find_coupon(db, body.code), user, now)
    cart = get_cart(db, user, now)
    cart.coupon_code = coupon.code
    cart.updated_at = now
    db.commit()
    return cart_out(db, cart)


@router.delete("/coupon", response_model=CartOut, summary="Remove the coupon")
def remove_coupon(user: CurrentUser, db: Db, clock: AppClock) -> CartOut:
    now = clock.now()
    cart = get_cart(db, user, now)
    cart.coupon_code = None
    cart.updated_at = now
    db.commit()
    return cart_out(db, cart)
