"""Cart rules, coupons, checkout with sandbox cards, and orders."""

import pytest

from .conftest import CARD_DECLINED, CARD_TIMEOUT, checkout, error_code

PLAYWRIGHT_BOOK = 4  # stock 3
SOLD_OUT = 5
INACTIVE = 13
PYTHON_BOOK = 6  # 39.99, stock 30


def add(client, headers, product_id, quantity=1):
    body = {"product_id": product_id, "quantity": quantity}
    return client.post("/api/cart/items", json=body, headers=headers)


def stock(client, product_id) -> int:
    return client.get(f"/api/products/{product_id}").json()["stock"]


def test_a_new_cart_is_empty(client, login):
    cart = client.get("/api/cart", headers=login()).json()
    assert cart["items"] == [] and cart["item_count"] == 0 and cart["total_cents"] == 0


def test_add_change_and_remove(client, login):
    headers = login()
    add(client, headers, PYTHON_BOOK)
    cart = add(client, headers, PYTHON_BOOK, 2).json()  # adds to the same line
    assert cart["items"][0]["quantity"] == 3
    assert cart["subtotal_cents"] == 3 * 3999

    cart = client.patch(f"/api/cart/items/{PYTHON_BOOK}", json={"quantity": 1}, headers=headers)
    assert cart.json()["item_count"] == 1

    cart = client.delete(f"/api/cart/items/{PYTHON_BOOK}", headers=headers)
    assert cart.json()["items"] == []
    missing = client.delete(f"/api/cart/items/{PYTHON_BOOK}", headers=headers)
    assert error_code(missing) == "ITEM_NOT_IN_CART"


def test_quantity_is_1_to_10(client, login):
    headers = login()
    assert add(client, headers, PYTHON_BOOK, 0).status_code == 422
    assert add(client, headers, PYTHON_BOOK, 11).status_code == 422
    add(client, headers, PYTHON_BOOK, 10)
    assert error_code(add(client, headers, PYTHON_BOOK, 1)) == "QUANTITY_LIMIT"


def test_you_cannot_add_more_than_the_stock(client, login):
    headers = login()
    assert add(client, headers, PLAYWRIGHT_BOOK, 3).status_code == 200
    too_many = add(client, headers, PLAYWRIGHT_BOOK, 1)
    assert too_many.status_code == 409
    assert too_many.json()["error"]["details"] == {"product_id": PLAYWRIGHT_BOOK, "stock": 3}
    assert error_code(add(client, headers, SOLD_OUT)) == "OUT_OF_STOCK"
    assert error_code(add(client, headers, INACTIVE)) == "PRODUCT_NOT_FOUND"


def test_the_cart_needs_a_login(client):
    assert client.get("/api/cart").status_code == 401


@pytest.mark.parametrize(("code", "check"), [
    ("WELCOME10", lambda cart: cart["discount_cents"] == 400),
    ("welcome10", lambda cart: cart["coupon_code"] == "WELCOME10"),
    ("FREESHIP", lambda cart: cart["shipping_cents"] == 0),
])  # fmt: skip
def test_coupons(client, login, code, check):
    headers = login()
    add(client, headers, PYTHON_BOOK)  # 39.99
    cart = client.post("/api/cart/coupon", json={"code": code}, headers=headers)
    assert cart.status_code == 200
    assert check(cart.json())


@pytest.mark.parametrize(("code", "error"), [
    ("SPRING25", "COUPON_EXPIRED"),
    ("NOPE", "COUPON_NOT_FOUND"),
])  # fmt: skip
def test_bad_coupons(client, login, code, error):
    response = client.post("/api/cart/coupon", json={"code": code}, headers=login())
    assert error_code(response) == error


def test_remove_the_coupon(client, login):
    headers = login()
    client.post("/api/cart/coupon", json={"code": "FREESHIP"}, headers=headers)
    assert client.delete("/api/cart/coupon", headers=headers).json()["coupon_code"] is None


def test_checkout_pays_takes_stock_and_empties_the_cart(client, login, outbox):
    headers = login()
    add(client, headers, PLAYWRIGHT_BOOK, 2)
    response = checkout(client, headers)
    assert response.status_code == 201
    order = response.json()
    assert order["status"] == "paid"
    assert order["total_cents"] == 2 * 3499 + 700 + 0  # 69.98 + tax, free shipping
    assert order["payments"][0]["status"] == "succeeded"
    assert order["payments"][0]["card_last4"] == "4242"
    assert order["shipping_address"] == "12 Test Street, Sample City"  # from the profile
    assert stock(client, PLAYWRIGHT_BOOK) == 1
    assert client.get("/api/cart", headers=headers).json()["items"] == []
    assert f"order {order['id']}" in outbox.last_to("arshad@example.com").subject


@pytest.mark.parametrize(("card", "status", "error", "payment"), [
    (CARD_DECLINED, 402, "PAYMENT_DECLINED", "declined"),
    (CARD_TIMEOUT, 504, "PAYMENT_TIMEOUT", "timeout"),
])  # fmt: skip
def test_failed_payment_keeps_the_cart_and_the_stock(client, login, card, status, error, payment):
    headers = login()
    add(client, headers, PLAYWRIGHT_BOOK, 2)
    response = checkout(client, headers, card)
    assert response.status_code == status
    assert error_code(response) == error
    order_id = response.json()["error"]["details"]["order_id"]

    order = client.get(f"/api/orders/{order_id}", headers=headers).json()
    assert order["status"] == "pending"
    assert order["payments"][0]["status"] == payment
    assert stock(client, PLAYWRIGHT_BOOK) == 3
    assert client.get("/api/cart", headers=headers).json()["item_count"] == 2


@pytest.mark.parametrize(("extra", "error"), [
    ({"card": "1234 5678 9012 3456"}, "INVALID_CARD"),
    ({"expiry": "01/20"}, "CARD_EXPIRED"),
])  # fmt: skip
def test_card_checks(client, login, extra, error):
    headers = login()
    add(client, headers, PYTHON_BOOK)
    card = extra.pop("card", "4242 4242 4242 4242")
    assert error_code(checkout(client, headers, card, **extra)) == error


def test_checkout_needs_items_and_an_address(client, login):
    headers = login()
    assert error_code(checkout(client, headers)) == "CART_EMPTY"
    client.patch("/api/users/me", json={"shipping_address": ""}, headers=headers)
    add(client, headers, PYTHON_BOOK)
    assert error_code(checkout(client, headers)) == "ADDRESS_REQUIRED"
    given = checkout(client, headers, shipping_address="9 Other Street, Sample City")
    assert given.status_code == 201


def test_stock_is_checked_again_at_checkout(client, login):
    headers = login()
    add(client, headers, PLAYWRIGHT_BOOK, 3)
    client.patch(f"/api/products/{PLAYWRIGHT_BOOK}", json={"stock": 1}, headers=login("admin"))
    assert error_code(checkout(client, headers)) == "OUT_OF_STOCK"


def test_a_product_hidden_after_adding_cannot_be_bought(client, login):
    headers = login()
    add(client, headers, PYTHON_BOOK)
    client.delete(f"/api/products/{PYTHON_BOOK}", headers=login("admin"))
    assert error_code(checkout(client, headers)) == "PRODUCT_UNAVAILABLE"


def test_welcome10_works_once_per_customer(client, login):
    headers = login()
    add(client, headers, PYTHON_BOOK)
    client.post("/api/cart/coupon", json={"code": "WELCOME10"}, headers=headers)
    order = checkout(client, headers).json()
    assert order["coupon_code"] == "WELCOME10" and order["discount_cents"] == 400
    again = client.post("/api/cart/coupon", json={"code": "WELCOME10"}, headers=headers)
    assert error_code(again) == "COUPON_ALREADY_USED"


def test_my_orders_newest_first_and_only_mine(client, login):
    headers = login()
    add(client, headers, PYTHON_BOOK)
    new_order = checkout(client, headers).json()
    orders = client.get("/api/orders", headers=headers).json()
    assert [o["id"] for o in orders["items"]] == [new_order["id"], 1]  # 1 is the seeded order
    maria_order = 2
    assert (
        error_code(client.get(f"/api/orders/{maria_order}", headers=headers)) == "ORDER_NOT_FOUND"
    )


def test_cancel_a_paid_order(client, login):
    headers = login()
    add(client, headers, PLAYWRIGHT_BOOK, 2)
    order_id = checkout(client, headers).json()["id"]
    cancelled = client.post(f"/api/orders/{order_id}/cancel", headers=headers).json()
    assert cancelled["status"] == "cancelled"
    assert cancelled["payments"][0]["status"] == "refunded"
    assert stock(client, PLAYWRIGHT_BOOK) == 3
    again = client.post(f"/api/orders/{order_id}/cancel", headers=headers)
    assert error_code(again) == "ORDER_NOT_CANCELLABLE"


def test_a_delivered_order_cannot_be_cancelled(client, login):
    response = client.post("/api/orders/1/cancel", headers=login())
    assert error_code(response) == "ORDER_NOT_CANCELLABLE"
