"""Categories, product search, filters, sorting, pages, admin changes and reviews."""

import pytest

from .conftest import error_code

ACTIVE_PRODUCTS = 12  # 13 seeded, one of them inactive


def names(response) -> list[str]:
    return [product["name"] for product in response.json()["items"]]


def test_categories(client):
    response = client.get("/api/categories")
    assert [c["slug"] for c in response.json()] == [
        "programming-books",
        "study-gadgets",
        "testing-books",
    ]


def test_list_shows_active_products_newest_first(client):
    body = client.get("/api/products").json()
    assert body["total"] == ACTIVE_PRODUCTS
    assert body["page"] == 1 and body["size"] == 20 and body["pages"] == 1
    dates = [p["created_at"] for p in body["items"]]
    assert dates == sorted(dates, reverse=True)
    assert "Old Model Book Light" not in names(client.get("/api/products"))


def test_inactive_products_are_hidden_except_for_admins(client, login):
    assert error_code(client.get("/api/products/13")) == "PRODUCT_NOT_FOUND"
    admin = login("admin")
    assert client.get("/api/products/13", headers=admin).status_code == 200
    everything = client.get("/api/products?include_inactive=true", headers=admin)
    assert everything.json()["total"] == ACTIVE_PRODUCTS + 1
    not_admin = client.get("/api/products?include_inactive=true", headers=login("arshad"))
    assert not_admin.json()["total"] == ACTIVE_PRODUCTS


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("q=python", {"Python for Testers", "API Testing with Python"}),
        ("q=PYTHON", {"Python for Testers", "API Testing with Python"}),
        ("q=%25", set()),  # a literal %, not "match anything"
        ("q=nothing-like-this", set()),
        ("category=study-gadgets&max_price_cents=1500", {"Pomodoro Desk Timer",
                                                        "Bug Hunter Sticky Notes (5 pack)"}),
        ("min_price_cents=3400&max_price_cents=4000", {"Python for Testers",
                                                       "Playwright Step by Step"}),
        ("in_stock=false", {"Exploratory Testing Notebook"}),
        ("category=no-such-category", set()),
    ],
)  # fmt: skip
def test_search_and_filters(client, query, expected):
    assert set(names(client.get(f"/api/products?{query}&size=50"))) == expected


def test_price_range_must_make_sense(client):
    response = client.get("/api/products?min_price_cents=500&max_price_cents=100")
    assert error_code(response) == "INVALID_PRICE_RANGE"


@pytest.mark.parametrize(("sort", "key", "reverse"), [
    ("price", "price_cents", False),
    ("-price", "price_cents", True),
    ("name", "name", False),
    ("-name", "name", True),
])  # fmt: skip
def test_sorting(client, sort, key, reverse):
    items = client.get(f"/api/products?sort={sort}&size=50").json()["items"]
    values = [item[key] for item in items]
    assert values == sorted(values, reverse=reverse)


def test_pages(client):
    body = client.get("/api/products?size=5&page=3").json()
    assert len(body["items"]) == 2 and body["pages"] == 3 and body["total"] == ACTIVE_PRODUCTS
    assert client.get("/api/products?size=5&page=4").json()["items"] == []


@pytest.mark.parametrize("query", ["size=51", "size=0", "page=0", "sort=cheapest"])
def test_bad_list_options_are_refused(client, query):
    assert client.get(f"/api/products?{query}").status_code == 422


def test_product_shows_stock_and_rating(client):
    product = client.get("/api/products/1").json()
    assert product["sku"] == "BK-TEST-001"
    assert product["rating_average"] == 4.0 and product["rating_count"] == 1
    sold_out = client.get("/api/products/5").json()
    assert sold_out["stock"] == 0 and sold_out["in_stock"] is False


def test_admin_adds_changes_and_hides_a_product(client, login):
    admin = login("admin")
    new = {"sku": "BK-NEW-001", "name": "Test Plans", "category_id": 1, "price_cents": 1500,
           "stock": 5}  # fmt: skip
    created = client.post("/api/products", json=new, headers=admin)
    assert created.status_code == 201
    product_id = created.json()["id"]
    assert error_code(client.post("/api/products", json=new, headers=admin)) == "SKU_TAKEN"

    changed = client.patch(f"/api/products/{product_id}", json={"price_cents": 1200}, headers=admin)
    assert changed.json()["price_cents"] == 1200

    assert client.delete(f"/api/products/{product_id}", headers=admin).status_code == 204
    assert client.get(f"/api/products/{product_id}").status_code == 404


def test_only_admins_change_products(client, login):
    new = {"sku": "BK-NEW-002", "name": "X", "category_id": 1, "price_cents": 100, "stock": 1}
    assert client.post("/api/products", json=new).status_code == 401
    assert client.post("/api/products", json=new, headers=login("arshad")).status_code == 403
    bad_category = client.post(
        "/api/products", json={**new, "category_id": 99}, headers=login("admin")
    )
    assert error_code(bad_category) == "CATEGORY_NOT_FOUND"


def test_reviews_are_listed_newest_first(client):
    reviews = client.get("/api/products/2/reviews").json()
    assert [r["username"] for r in reviews] == ["maria"]


def test_only_buyers_can_review_and_only_once(client, login):
    headers = login("arshad")
    review = {"rating": 5, "text": "Very handy."}
    not_bought = client.post("/api/products/2/reviews", json=review, headers=headers)
    assert error_code(not_bought) == "NOT_A_BUYER"

    bought = client.post("/api/products/8/reviews", json=review, headers=headers)  # seeded order
    assert bought.status_code == 201
    again = client.post("/api/products/8/reviews", json=review, headers=headers)
    assert error_code(again) == "ALREADY_REVIEWED"


@pytest.mark.parametrize("review", [
    {"rating": 0, "text": "ok"},
    {"rating": 6, "text": "ok"},
    {"rating": 3, "text": ""},
    {"rating": 3, "text": "   "},
    {"rating": 3, "text": "x" * 501},
])  # fmt: skip
def test_review_rules(client, login, review):
    response = client.post("/api/products/8/reviews", json=review, headers=login("arshad"))
    assert response.status_code == 422
