"""The Bug Hunt switch: each planted bug is there when PRACTICE_APP_BUGS is on,
and gone when it is off. The answers are in BUG_HUNT_ANSWERS.md (spoilers)."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from bookshelf import bugs, money
from bookshelf.reporting import DailySale

from .conftest import PASSWORD, checkout, code_in, error_code, make_app

MARIA_ORDER = 2
PYTHON_BOOK = 6


@pytest.fixture(params=[True, False], ids=["bugs-on", "bugs-off"])
def shop(request):
    app = make_app(planted_bugs=request.param)
    with TestClient(app) as client:
        yield app, client, request.param
    bugs.switch(False)


def login(client, username="arshad", password=PASSWORD) -> dict:
    token = client.post("/api/auth/login", json={"username": username, "password": password})
    return {"Authorization": f"Bearer {token.json()['access_token']}"}


def test_bh01_free_shipping_at_exactly_50_dollars():
    bugs.switch(True)
    assert money.calculate(5000).shipping_cents == 499
    bugs.switch(False)
    assert money.calculate(5000).shipping_cents == 0


def test_bh02_page_count(shop):
    _app, client, on = shop
    result = client.get("/api/products?size=5").json()
    assert result["total"] == 12
    assert result["pages"] == (2 if on else 3)


def test_bh03_daily_sales_and_cancelled_orders(shop):
    app, client, on = shop
    headers = login(client)
    admin = login(client, "admin", "local_only_password")

    def revenue() -> int:
        client.post("/api/admin/reporting/sync", headers=admin)
        with app.state.reporting_sessionmaker() as session:
            return session.scalar(select(func.sum(DailySale.revenue_cents))) or 0

    client.post("/api/cart/items", json={"product_id": PYTHON_BOOK, "quantity": 1}, headers=headers)
    order = checkout(client, headers).json()
    before = revenue()
    client.post(f"/api/orders/{order['id']}/cancel", headers=headers)
    after = revenue()
    assert after == (before if on else before - order["total_cents"])


def test_bh04_invoice_of_someone_elses_order(shop):
    _app, client, on = shop
    response = client.get(f"/api/orders/{MARIA_ORDER}/invoice.pdf", headers=login(client))
    if on:
        assert response.status_code == 200
    else:
        assert error_code(response) == "ORDER_NOT_FOUND"


def test_bh05_cart_badge(shop):
    _app, client, on = shop
    client.get("/login")
    csrf = client.cookies["bookshelf_csrf"]
    client.post("/login", data={"username": "arshad", "password": PASSWORD, "csrf_token": csrf})
    client.post("/cart/items", data={"product_id": "6", "quantity": "3", "csrf_token": csrf})
    badge = '<span class="badge" data-testid="nav-cart-count">{}</span>'
    assert badge.format(1 if on else 3) in client.get("/").text


def test_bh06_old_reset_code(shop):
    app, client, on = shop
    client.post("/api/auth/forgot-password", json={"email": "arshad@example.com"})
    code = code_in(app.state.outbox.last_to("arshad@example.com"))
    app.state.clock.advance(11 * 60)  # the code lasts 10 minutes
    body = {"email": "arshad@example.com", "code": code, "new_password": "New@12345"}
    response = client.post("/api/auth/reset-password", json=body)
    if on:
        assert response.status_code == 200
    else:
        assert error_code(response) == "CODE_EXPIRED"
