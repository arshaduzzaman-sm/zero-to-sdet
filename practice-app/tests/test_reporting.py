"""The reporting copy: orders copied to order_facts and daily_sales."""

from datetime import date

from sqlalchemy import select

from bookshelf.reporting import DailySale, OrderFact

from .conftest import checkout, error_code


def facts(app) -> dict[int, OrderFact]:
    with app.state.reporting_sessionmaker() as session:
        return {fact.order_id: fact for fact in session.scalars(select(OrderFact))}


def daily(app) -> dict[date, DailySale]:
    with app.state.reporting_sessionmaker() as session:
        return {day.sales_date: day for day in session.scalars(select(DailySale))}


def test_the_copy_starts_with_the_seed_orders(app, client):
    copied = facts(app)
    assert set(copied) == {1, 2}
    assert copied[1].customer_email == "arshad@example.com"
    assert copied[1].item_count == 3
    assert daily(app)[date(2026, 2, 10)].revenue_cents == copied[1].total_cents


def test_a_new_order_appears_only_after_a_sync(app, client, login):
    headers = login()
    client.post("/api/cart/items", json={"product_id": 6, "quantity": 2}, headers=headers)
    order = checkout(client, headers).json()
    assert order["id"] not in facts(app)  # the copy is behind until the next sync

    synced = client.post("/api/admin/reporting/sync", headers=login("admin"))
    assert synced.status_code == 200
    assert synced.json()["orders"] == 3

    fact = facts(app)[order["id"]]
    assert fact.total_cents == order["total_cents"]
    assert fact.status == "paid" and fact.item_count == 2


def test_daily_sales_count_only_real_sales(app, client, login):
    headers = login()
    client.post("/api/cart/items", json={"product_id": 6}, headers=headers)
    declined = checkout(client, headers, "4000 0000 0000 0002")
    assert error_code(declined) == "PAYMENT_DECLINED"
    client.post("/api/admin/reporting/sync", headers=login("admin"))

    pending = facts(app)[declined.json()["error"]["details"]["order_id"]]
    assert pending.status == "pending"
    total_sold = sum(day.revenue_cents for day in daily(app).values())
    assert total_sold == facts(app)[1].total_cents + facts(app)[2].total_cents


def test_only_admins_can_sync(client, login):
    assert client.post("/api/admin/reporting/sync", headers=login()).status_code == 403
