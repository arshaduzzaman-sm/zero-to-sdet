"""Admin tools (orders, status, reset, clock) and tester tools (health, version, request IDs)."""

from datetime import UTC, datetime

from .conftest import checkout, error_code


def paid_order(client, login) -> int:
    headers = login()
    client.post("/api/cart/items", json={"product_id": 6}, headers=headers)
    return checkout(client, headers).json()["id"]


def test_admin_sees_every_order_and_can_filter(client, login):
    admin = login("admin")
    assert client.get("/api/admin/orders", headers=admin).json()["total"] == 2
    delivered = client.get("/api/admin/orders?status=delivered", headers=admin).json()
    assert {o["status"] for o in delivered["items"]} == {"delivered"}
    assert client.get("/api/admin/orders", headers=login("arshad")).status_code == 403


def test_orders_move_one_step_at_a_time(client, login):
    order_id = paid_order(client, login)
    admin = login("admin")
    skip = client.patch(
        f"/api/admin/orders/{order_id}", json={"status": "delivered"}, headers=admin
    )
    assert error_code(skip) == "INVALID_STATUS_CHANGE"
    for status in ("shipped", "delivered"):
        response = client.patch(
            f"/api/admin/orders/{order_id}", json={"status": status}, headers=admin
        )
        assert response.json()["status"] == status
    bad = client.patch(f"/api/admin/orders/{order_id}", json={"status": "paid"}, headers=admin)
    assert bad.status_code == 422  # only "shipped" or "delivered" can be sent


def test_admin_lists_users(client, login):
    users = client.get("/api/users", headers=login("admin")).json()
    assert [u["username"] for u in users["items"]] == ["arshad", "maria", "admin"]
    assert client.get("/api/users", headers=login("maria")).status_code == 403


def test_reset_puts_the_data_back(client, login):
    paid_order(client, login)
    client.post("/api/auth/signup", json={"email": "temp@example.com", "username": "temp",
                                          "full_name": "Temp", "password": "Temp1234"})  # fmt: skip
    response = client.post("/api/admin/reset", headers=login("admin"))
    assert response.status_code == 200
    assert client.get("/api/products/6").json()["stock"] == 30
    assert client.get("/api/admin/orders", headers=login("admin")).json()["total"] == 2
    unknown = client.post("/api/auth/login", json={"username": "temp", "password": "Temp1234"})
    assert unknown.status_code == 401


def test_the_clock_can_jump_move_and_go_back(client, login):
    admin = login("admin")
    jumped = client.post("/api/admin/clock", json={"now": "2031-01-01T00:00:00Z"}, headers=admin)
    assert jumped.json()["now"].startswith("2031-01-01")
    assert jumped.json()["is_real_time"] is False

    # In 2031, WELCOME10 (ends 2030-12-31) has ended.
    coupon = client.post("/api/cart/coupon", json={"code": "WELCOME10"}, headers=login())
    assert error_code(coupon) == "COUPON_EXPIRED"

    admin = login("admin")  # tokens follow the app clock, so log in again after a jump
    moved = client.post("/api/admin/clock", json={"advance_seconds": 3600}, headers=admin)
    assert moved.json()["now"].startswith("2031-01-01T01:00")

    # Moving an hour ahead also expired that 30-minute token.
    assert client.get("/api/auth/me", headers=admin).status_code == 401
    back = client.post("/api/admin/clock", json={}, headers=login("admin")).json()
    assert back["is_real_time"] is True
    assert abs(datetime.fromisoformat(back["now"]) - datetime.now(UTC)).total_seconds() < 5


def test_clock_rules(client, login, app):
    admin = login("admin")
    both = {"now": "2031-01-01T00:00:00Z", "advance_seconds": 60}
    assert error_code(client.post("/api/admin/clock", json=both, headers=admin)) == "CLOCK_CONFLICT"
    assert client.post("/api/admin/clock", json={}, headers=login("arshad")).status_code == 403
    app.state.settings.clock_control = False
    response = client.post("/api/admin/clock", json={"advance_seconds": 60}, headers=admin)
    assert error_code(response) == "CLOCK_CONTROL_OFF"


def test_health_and_version(client):
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert health.json()["services"] == {
        "api": "up",
        "main_database": "up",
        "reporting_database": "up",
        "reviews_database": "up",
    }
    version = client.get("/api/version").json()
    assert version["version"] == "1.0.0"
    assert set(version["databases"]) == {"main", "reporting", "reviews"}


def test_every_response_has_a_request_id(client):
    generated = client.get("/api/health").headers["X-Request-ID"]
    assert len(generated) == 32

    mine = client.get("/api/health", headers={"X-Request-ID": "my-test-42"})
    assert mine.headers["X-Request-ID"] == "my-test-42"

    unsafe = client.get("/api/health", headers={"X-Request-ID": "bad id <script>"})
    assert unsafe.headers["X-Request-ID"] != "bad id <script>"


def test_errors_have_one_shape(client):
    response = client.get("/api/no-such-thing", headers={"X-Request-ID": "trace-me"})
    assert response.status_code == 404
    assert response.json() == {
        "error": {"code": "NOT_FOUND", "message": "Not Found", "request_id": "trace-me"}
    }
    wrong_method = client.delete("/api/health")
    assert error_code(wrong_method) == "METHOD_NOT_ALLOWED"


def test_api_docs_are_served(client):
    assert client.get("/docs").status_code == 200
    spec = client.get("/openapi.json").json()
    assert "/api/checkout" in spec["paths"]
    assert client.get("/", follow_redirects=False).headers["location"] == "/docs"
