"""The reporting copy: a second database with order facts and daily sales.

Lessons compare the same order in two databases (multi-database testing). The
sync copies orders from the main database here: every minute by itself
(REPORTING_SYNC_SECONDS), or right away with POST /api/admin/reporting/sync.
So for up to a minute the copy can be behind: tests must wait for it, or sync.

Each sync rebuilds both tables in one transaction, so a reader never sees half
a sync.
"""

from __future__ import annotations

import logging
import threading
from collections import defaultdict
from datetime import date, datetime

from sqlalchemy import Date, String, delete, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .db import UTCDateTime
from .models import Order, OrderItem, User

log = logging.getLogger("bookshelf.reporting")

SOLD = ("paid", "shipped", "delivered")  # what counts as a sale


class ReportingBase(DeclarativeBase):
    type_annotation_map = {datetime: UTCDateTime, date: Date}


class OrderFact(ReportingBase):
    __tablename__ = "order_facts"

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    customer_email: Mapped[str] = mapped_column(String(254), index=True)
    status: Mapped[str] = mapped_column(String(20))
    item_count: Mapped[int]
    total_cents: Mapped[int]
    created_at: Mapped[datetime]
    synced_at: Mapped[datetime]


class DailySale(ReportingBase):
    __tablename__ = "daily_sales"

    sales_date: Mapped[date] = mapped_column(primary_key=True)
    orders_count: Mapped[int]
    revenue_cents: Mapped[int]


def sync(main: sessionmaker, reporting: sessionmaker, now: datetime) -> dict:
    """Copy every order into the reporting tables. Returns what was copied."""
    with main() as session:
        rows = session.execute(
            select(
                Order.id,
                User.email,
                Order.status,
                func.coalesce(func.sum(OrderItem.quantity), 0),
                Order.total_cents,
                Order.created_at,
            )
            .join(User, User.id == Order.user_id)
            .outerjoin(OrderItem, OrderItem.order_id == Order.id)
            .group_by(Order.id, User.email, Order.status, Order.total_cents, Order.created_at)
            .order_by(Order.id)
        ).all()

    facts = []
    days: dict[date, list[int]] = defaultdict(lambda: [0, 0])
    for order_id, email, status, item_count, total, created_at in rows:
        facts.append(
            OrderFact(
                order_id=order_id,
                customer_email=email,
                status=status,
                item_count=int(item_count),
                total_cents=total,
                created_at=created_at,
                synced_at=now,
            )
        )
        if status in SOLD:
            day = days[created_at.date()]
            day[0] += 1
            day[1] += total

    with reporting() as session, session.begin():
        session.execute(delete(OrderFact))
        session.execute(delete(DailySale))
        session.add_all(facts)
        session.add_all(
            DailySale(sales_date=day, orders_count=count, revenue_cents=revenue)
            for day, (count, revenue) in sorted(days.items())
        )
    return {"orders": len(facts), "days": len(days), "synced_at": now}


class SyncLoop:
    """Runs the sync every few seconds in a background thread."""

    def __init__(self, run, seconds: int) -> None:
        self.run = run
        self.seconds = seconds
        self.stop_event = threading.Event()
        self.thread: threading.Thread | None = None

    def start(self) -> None:
        if self.seconds > 0:
            self.thread = threading.Thread(target=self._loop, name="reporting-sync", daemon=True)
            self.thread.start()

    def _loop(self) -> None:
        while not self.stop_event.wait(self.seconds):
            try:
                self.run()
            except Exception:  # keep the loop alive; the next run tries again
                log.exception("Reporting sync failed")

    def stop(self) -> None:
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=5)
