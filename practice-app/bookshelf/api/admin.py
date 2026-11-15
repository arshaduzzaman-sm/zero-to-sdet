"""Admin tools: every order, order status, reset the data, move the clock."""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Query, Request
from sqlalchemy import func, select

from ..database import reset_data, sync_reporting
from ..deps import AdminUser, AppClock, AppSettings, Db, PageNumber, PageSize, page_count
from ..errors import ApiError
from ..models import Order
from ..schemas import ClockIn, ClockOut, Message, OrderOut, OrderStatusIn, Page, SyncOut
from .orders import order_out

router = APIRouter(prefix="/admin", tags=["Admin"])

NEXT_STATUS = {"paid": "shipped", "shipped": "delivered"}

Status = Literal["pending", "paid", "shipped", "delivered", "cancelled"]


@router.get("/orders", response_model=Page[OrderOut], summary="List every order")
def all_orders(
    _admin: AdminUser,
    db: Db,
    status: Annotated[Status | None, Query()] = None,
    page: PageNumber = 1,
    size: PageSize = 20,
) -> dict:
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
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


@router.patch("/orders/{order_id}", response_model=OrderOut, summary="Ship or deliver an order")
def change_status(
    order_id: int, body: OrderStatusIn, _admin: AdminUser, db: Db, clock: AppClock
) -> OrderOut:
    """Orders move one step at a time: paid -> shipped -> delivered."""
    order = db.get(Order, order_id)
    if order is None:
        raise ApiError(404, "ORDER_NOT_FOUND", "Order not found.")
    if NEXT_STATUS.get(order.status) != body.status:
        raise ApiError(
            409,
            "INVALID_STATUS_CHANGE",
            f"An order that is {order.status} cannot become {body.status}.",
        )
    order.status = body.status
    order.updated_at = clock.now()
    db.commit()
    return order_out(order)


@router.post("/reset", response_model=Message, summary="Put all data back to the start")
def reset(_admin: AdminUser, db: Db, request: Request, clock: AppClock) -> Message:
    """Deletes everything (new accounts, carts, orders, reviews) and loads the seed
    data again. The clock goes back to real time."""
    # This request already read the users table (to check the admin). On PostgreSQL
    # and MySQL that read holds a lock until the transaction ends, and DROP TABLE
    # would wait for it forever. So end this request's transaction first.
    db.rollback()
    db.close()
    reset_data(request.app)
    clock.reset()
    return Message(message="All data is back to the start.")


@router.post("/reporting/sync", response_model=SyncOut, summary="Refresh the reporting copy now")
def reporting_sync(_admin: AdminUser, request: Request) -> dict:
    """Copies every order into the reporting database (order_facts, daily_sales).
    It also runs by itself every minute."""
    return sync_reporting(request.app)


def clock_allowed(settings) -> None:
    if not settings.clock_control:
        raise ApiError(403, "CLOCK_CONTROL_OFF", "Clock control is turned off (CLOCK_CONTROL).")


@router.get("/clock", response_model=ClockOut, summary="What time does the app think it is?")
def read_clock(_admin: AdminUser, clock: AppClock) -> ClockOut:
    return ClockOut(now=clock.now(), is_real_time=clock.is_real)


@router.post("/clock", response_model=ClockOut, summary="Move the app's clock")
def set_clock(body: ClockIn, _admin: AdminUser, clock: AppClock, settings: AppSettings) -> ClockOut:
    """Send `now` to jump to a time, `advance_seconds` to move forward, or nothing to go
    back to real time. The clock keeps ticking from the new time."""
    clock_allowed(settings)
    if body.now is not None and body.advance_seconds is not None:
        raise ApiError(400, "CLOCK_CONFLICT", "Send now or advance_seconds, not both.")
    if body.now is not None:
        clock.set(body.now)
    elif body.advance_seconds is not None:
        clock.advance(body.advance_seconds)
    else:
        clock.reset()
    return ClockOut(now=clock.now(), is_real_time=clock.is_real)
