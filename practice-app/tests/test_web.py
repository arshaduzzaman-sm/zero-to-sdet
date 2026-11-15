"""The web pages: forms, login cookie, CSRF, escaping, and a data-testid on everything."""

from html.parser import HTMLParser

import pytest

from .conftest import PASSWORD, code_in


def csrf(client) -> str:
    client.get("/login")  # any page sets the CSRF cookie
    return client.cookies["bookshelf_csrf"]


def post(client, path: str, data: dict | None = None):
    return client.post(path, data={**(data or {}), "csrf_token": csrf(client)},
                       follow_redirects=False)  # fmt: skip


def web_login(client, username="arshad", password=PASSWORD):
    response = post(client, "/login", {"username": username, "password": password, "next": "/"})
    assert response.status_code == 303, response.text
    return response


class MissingTestIds(HTMLParser):
    """Collects interactive elements that have no data-testid."""

    INTERACTIVE = {"a", "button", "input", "select", "textarea", "form"}

    def __init__(self) -> None:
        super().__init__()
        self.missing: list[str] = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag not in self.INTERACTIVE or attributes.get("type") == "hidden":
            return
        if "data-testid" not in attributes:
            self.missing.append(f"<{tag} {attributes}>")


def test_the_shop_lists_products(client):
    page = client.get("/")
    assert page.status_code == 200
    assert page.text.count('data-testid="product-card"') == 12
    assert "Old Model Book Light" not in page.text  # inactive


def test_search_and_a_friendly_price_error(client):
    found = client.get("/?q=python")
    assert found.text.count('data-testid="product-card"') == 2
    bad = client.get("/?min_price=abc")
    assert bad.status_code == 200
    assert 'data-testid="min-price-error"' in bad.text


def test_pages_that_need_a_login_send_you_to_log_in(client):
    response = client.get("/cart", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login?next=/cart&msg=login_needed"


def test_log_in_sets_a_safe_cookie(client):
    wrong = post(client, "/login", {"username": "arshad", "password": "nope"})
    assert wrong.status_code == 400
    assert 'data-testid="form-error"' in wrong.text

    response = web_login(client)
    cookie = response.headers["set-cookie"].lower()
    assert "bookshelf_session=" in cookie and "httponly" in cookie and "samesite=lax" in cookie
    assert 'data-testid="nav-profile">arshad<' in client.get("/").text


@pytest.mark.parametrize("target", ["https://evil.example", "//evil.example", "/\\evil.example"])
def test_login_never_sends_you_to_another_site(client, target):
    response = post(client, "/login", {"username": "arshad", "password": PASSWORD, "next": target})
    assert response.headers["location"].startswith("/?")


def test_forms_without_the_csrf_token_are_refused(client):
    client.get("/login")
    missing = client.post("/login", data={"username": "arshad", "password": PASSWORD})
    assert missing.status_code == 403
    assert 'data-testid="error-page"' in missing.text
    wrong = client.post(
        "/login", data={"username": "arshad", "password": PASSWORD, "csrf_token": "guess"}
    )
    assert wrong.status_code == 403


def test_shop_from_cart_to_cancelled_order(client):
    web_login(client)
    assert post(client, "/cart/items", {"product_id": "6", "quantity": "2"}).status_code == 303
    cart = client.get("/cart").text
    assert 'data-testid="cart-total">$87.98<' in cart  # 2 x 39.99 + 10% tax, free shipping

    post(client, "/cart/coupon", {"code": "welcome10", "action": "apply"})
    assert 'data-testid="applied-coupon">WELCOME10<' in client.get("/cart").text

    placed = post(client, "/checkout", {"shipping_address": "1 Test Lane",
                                        "card_number": "4242 4242 4242 4242",
                                        "expiry": "12/30", "cvc": "123"})  # fmt: skip
    assert placed.status_code == 303
    order_url = placed.headers["location"].split("?")[0]
    order = client.get(order_url).text
    assert 'data-testid="order-status">paid<' in order
    assert 'data-testid="nav-cart-count">0<' in order

    post(client, f"{order_url}/cancel")
    assert 'data-testid="order-status">cancelled<' in client.get(order_url).text


def test_a_declined_card_shows_an_error_and_never_echoes_card_data(client):
    web_login(client)
    post(client, "/cart/items", {"product_id": "6"})
    response = post(client, "/checkout", {"shipping_address": "1 Test Lane",
                                          "card_number": "4000 0000 0000 0002",
                                          "expiry": "12/30", "cvc": "987"})  # fmt: skip
    assert response.status_code == 400
    assert "The card was declined." in response.text
    assert "4000 0000 0000 0002" not in response.text and 'value="987"' not in response.text
    assert 'data-testid="cart-line"' in client.get("/cart").text  # the cart is kept


def test_sign_up_verify_and_log_in_on_the_web(client, outbox):
    form = {"email": "web.tester@example.com", "username": "web_tester",
            "full_name": "Web Tester", "password": "Secret123"}  # fmt: skip
    created = post(client, "/signup", form)
    assert created.headers["location"].startswith("/verify?email=web.tester%40example.com")
    code = code_in(outbox.last_to("web.tester@example.com"))
    verified = post(client, "/verify", {"email": form["email"], "code": code, "action": "verify"})
    assert verified.headers["location"] == "/login?msg=verified"
    web_login(client, "web_tester", "Secret123")


def test_sign_up_errors_show_next_to_the_field_and_keep_the_password_out(client):
    response = post(client, "/signup", {"email": "bad", "username": "x", "full_name": "Me",
                                        "password": "Secret123"})  # fmt: skip
    assert response.status_code == 400
    assert 'data-testid="email-error"' in response.text
    assert 'data-testid="username-error"' in response.text
    assert "Secret123" not in response.text


def test_review_text_is_escaped(client, login):
    client.post("/api/products/8/reviews", json={"rating": 5, "text": "<script>alert(1)</script>"},
                headers=login())  # fmt: skip
    page = client.get("/products/8").text
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page


def test_admin_page_is_for_admins_only(client):
    web_login(client)
    assert client.get("/admin").status_code == 403
    post(client, "/logout")
    web_login(client, "admin", "local_only_password")
    assert client.get("/admin").status_code == 200

    saved = post(client, "/admin/products/4", {"stock": "7", "is_active": "on"})
    assert saved.status_code == 303
    assert client.get("/api/products/4").json()["stock"] == 7
    assert post(client, "/admin/reset").status_code == 303
    assert client.get("/api/products/4").json()["stock"] == 3


def test_errors_are_pages_on_the_web_and_json_in_the_api(client):
    page = client.get("/no-such-page")
    assert page.status_code == 404 and 'data-testid="error-page"' in page.text
    product = client.get("/products/999")
    assert product.status_code == 404 and "Product not found." in product.text
    api = client.get("/api/products/999")
    assert api.json()["error"]["code"] == "PRODUCT_NOT_FOUND"


def test_web_pages_send_security_headers(client):
    headers = client.get("/").headers
    assert "script-src 'self'" in headers["content-security-policy"]
    assert headers["x-frame-options"] == "DENY"


def test_an_expired_session_asks_to_log_in_again(client, clock):
    web_login(client)
    clock.advance(31 * 60)
    response = client.get("/orders", follow_redirects=False)
    assert response.headers["location"].endswith("msg=session_expired")


def test_log_out(client):
    web_login(client)
    post(client, "/logout")
    assert 'data-testid="nav-login"' in client.get("/").text


def test_every_interactive_element_has_a_test_id(client):
    pages = ["/login", "/signup", "/verify", "/forgot-password", "/reset-password", "/",
             "/?page=1&q=a", "/products/1", "/no-such-page"]  # fmt: skip
    signed_in = ["/", "/products/8", "/cart", "/checkout", "/orders", "/orders/1", "/profile"]
    missing: dict[str, list[str]] = {}

    def check(path: str) -> None:
        parser = MissingTestIds()
        parser.feed(client.get(path).text)
        if parser.missing:
            missing[path] = parser.missing

    for path in pages:
        check(path)
    web_login(client)
    post(client, "/cart/items", {"product_id": "6"})
    for path in signed_in:
        check(path)
    post(client, "/logout")
    web_login(client, "admin", "local_only_password")
    check("/admin")
    assert missing == {}
