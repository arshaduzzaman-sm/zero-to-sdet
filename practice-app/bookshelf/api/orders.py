"""Checkout with a sandbox card, and your orders."""

from __future__ import annotations

import secrets
import time
from datetime import UTC, datetime

from fastapi import APIRouter, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..deps import (
    AppClock,
    AppOutbox,
    AppSettings,
    CurrentUser,
    Db,
    PageNumber,
    PageSize,
    page_count,
)
from ..errors import ApiError
from ..invoice import build_invoice
from ..models import CouponUse, Order, OrderItem, Payment, Product
from ..schemas import CheckoutIn, OrderLineOut, OrderOut, Page, PaymentOut
from .cart import cart_totals, check_coupon, find_coupon, get_cart

router = APIRouter(tags=["Checkout and orders"])

# The only cards the sandbox knows (DESIGN.md section 2).
SANDBOX_CARDS = {
    "4242424242424242": "succeeded",
    "4000000000000002": "declined",
    "4000000000009995": "timeout",
}


def order_out(order: Order) -> OrderOut:
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        items=[
            OrderLineOut(
                product_id=item.product_id,
                sku=item.product.sku,
                name=item.product.name,
                quantity=item.quantity,
                unit_price_cents=item.unit_price_cents,
                line_total_cents=item.unit_price_cents * item.quantity,
            )
            for item in order.items
        ],
        coupon_code=order.coupon_code,
        subtotal_cents=order.subtotal_cents,
        discount_cents=order.discount_cents,
        tax_cents=order.tax_cents,
        shipping_cents=order.shipping_cents,
        total_cents=order.total_cents,
        shipping_address=order.shipping_address,
        payments=[PaymentOut.model_validate(p) for p in order.payments],
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


def card_outcome(card_number: str, expiry: str, now: datetime) -> tuple[str, str]:
    digits = card_number.replace(" ", "").replace("-", "")
    if digits not in SANDBOX_CARDS:
        raise ApiError(
            400,
            "INVALID_CARD",
            "Use a sandbox card: 4242 4242 4242 4242, 4000 0000 0000 0002 or 4000 0000 0000 9995.",
        )
    month, year = (int(part) for part in expiry.split("/"))
    first_of_next = datetime(2000 + year + month // 12, month % 12 + 1, 1, tzinfo=UTC)
    if first_of_next <= now:
        raise ApiError(400, "CARD_EXPIRED", "This card has expired.")
    return SANDBOX_CARDS[digits], digits[-4:]


def own_order(db: Session, order_id: int, user_id: int) -> Order:
    order = db.get(Order, order_id)
    if order is None or order.user_id != user_id:  # someone else's order looks like no order
        raise ApiError(404, "ORDER_NOT_FOUND", "Order not found.")
    return order


@router.post("/checkout", status_code=201, response_model=OrderOut, summary="Pay for my cart")
def checkout(
    body: CheckoutIn,
    user: CurrentUser,
    db: Db,
    clock: AppClock,
    settings: AppSettings,
    outbox: AppOutbox,
) -> OrderOut:
    """Creates an order from the cart and pays with a sandbox card.

    - Payment succeeds: the order is `paid`, stock goes down, the cart is emptied
      and a confirmation email is sent.
    - Declined (402) or timed out (504): the order stays `pending`, the cart and
      the stock do not change. You can try again.
    """
    now = clock.now()
    cart = get_cart(db, user, now)
    if not cart.items:
        raise ApiError(400, "CART_EMPTY", "Your cart is empty.")
    address = (body.shipping_address or user.shipping_address or "").strip()
    if not address:
        raise ApiError(400, "ADDRESS_REQUIRED", "Add a shipping address.")
    outcome, last4 = card_outcome(body.card_number, body.expiry, now)

    for item in cart.items:
        product = db.scalars(
            select(Product).where(Product.id == item.product_id).with_for_update()
        ).one()
        if not product.is_active:
            raise ApiError(
                409,
                "PRODUCT_UNAVAILABLE",
                f"{product.name} is no longer sold. Remove it from your cart.",
                details={"product_id": product.id},
            )
        if item.quantity > product.stock:
            raise ApiError(
                409,
                "OUT_OF_STOCK",
                f"Sorry, only {product.stock} left of {product.name}.",
                details={"product_id": product.id, "stock": product.stock},
            )
    coupon = None
    if cart.coupon_code:
        coupon = check_coupon(db, find_coupon(db, cart.coupon_code), user, now)
    totals = cart_totals(db, cart)

    order = Order(
        user_id=user.id,
        status="pending",
        coupon_code=coupon.code if coupon else None,
        shipping_address=address,
        created_at=now,
        updated_at=now,
        **totals.as_dict(),
    )
    order.items = [
        OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price_cents=item.product.price_cents,
        )
        for item in cart.items
    ]
    db.add(order)
    db.flush()

    if outcome == "timeout":
        time.sleep(settings.payment_timeout_seconds)
    payment = Payment(
        order_id=order.id,
        card_last4=last4,
        status=outcome,
        amount_cents=totals.total_cents,
        sandbox_ref=f"sbx_{secrets.token_hex(8)}",
        created_at=now,
    )
    db.add(payment)

    if outcome == "declined":
        db.commit()
        raise ApiError(
            402, "PAYMENT_DECLINED", "The card was declined.", details={"order_id": order.id}
        )
    if outcome == "timeout":
        db.commit()
        raise ApiError(
            504,
            "PAYMENT_TIMEOUT",
            "The payment service did not answer in time. Try again.",
            details={"order_id": order.id},
        )

    for item in cart.items:
        item.product.stock -= item.quantity
    if coupon is not None:
        db.add(CouponUse(coupon_id=coupon.id, user_id=user.id, order_id=order.id))
    order.status = "paid"
    cart.items.clear()
    cart.coupon_code = None
    cart.updated_at = now
    db.commit()
    db.refresh(order)
    outbox.send(
        user.email,
        f"Bookshelf order {order.id} is confirmed",
        f"Hello {user.full_name},\n\nThank you! We got your order {order.id}.\n"
        f"Total paid: {order.total_cents / 100:.2f}\nShipping to: {order.shipping_address}",
        now,
    )
    return order_out(order)


@router.get("/orders", response_model=Page[OrderOut], summary="List my orders, newest first")
def list_orders(user: CurrentUser, db: Db, page: PageNumber = 1, size: PageSize = 20) -> dict:
    query = select(Order).where(Order.user_id == user.id)
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    newest_first = query.order_by(Order.created_at.desc(), Order.id.desc())
    orders = db.scalars(newest_first.offset((page - 1) * size).limit(size)).all()
    return {
        "items": [order_out(o) for o in orders],
        "page": page,
        "size": size,
        "total": total,
        "pages": page_count(total, size),
    }


@router.get("/orders/{order_id}", response_model=OrderOut, summary="Get one of my orders")
def get_order(order_id: int, user: CurrentUser, db: Db) -> OrderOut:
    return order_out(own_order(db, order_id, user.id))


@router.get(
    "/orders/{order_id}/invoice.pdf",
    response_class=Response,
    summary="Download the invoice of my order (PDF)",
    responses={200: {"content": {"application/pdf": {}}}},
)
def order_invoice(order_id: int, user: CurrentUser, db: Db) -> Response:
    """Only for orders that were paid (also after they are shipped, delivered or
    cancelled). An unpaid (pending) order has no invoice."""
    order = own_order(db, order_id, user.id)
    if order.status == "pending":
        raise ApiError(
            409, "INVOICE_NOT_AVAILABLE", "This order was not paid, so it has no invoice."
        )
    return Response(
        build_invoice(order),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="bookshelf-invoice-{order.id}.pdf"',
            "Cache-Control": "private, no-store",
        },
    )


@router.post("/orders/{order_id}/cancel", response_model=OrderOut, summary="Cancel my order")
def cancel_order(order_id: int, user: CurrentUser, db: Db, clock: AppClock) -> OrderOut:
    """Only a `paid` order (not yet shipped) can be cancelled. The stock goes back
    and the payment is marked refunded."""
    order = own_order(db, order_id, user.id)
    if order.status != "paid":
        raise ApiError(
            409,
            "ORDER_NOT_CANCELLABLE",
            f"An order that is {order.status} cannot be cancelled.",
        )
    now = clock.now()
    for item in order.items:
        item.product.stock += item.quantity
    for payment in order.payments:
        if payment.status == "succeeded":
            payment.status = "refunded"
    order.status = "cancelled"
    order.updated_at = now
    db.commit()
    return order_out(order)
