"""The starting data. It is the same on every start and after every reset, so
lessons can say "log in as arshad" or "product 4 has only 3 left".

Two parts, all fake:
1. Fixed data written out below: 3 users, 3 categories, 13 products, 3 coupons,
   2 delivered orders with reviews. Lessons rely on these exact values.
2. Faker data: 40 more customers (FAKE_CUSTOMERS) with orders and reviews, for
   lessons that need volume (search, pages, reports, performance). Faker and
   the random choices use a fixed seed (FAKER_SEED), so this data is also the
   same on every computer. Emails are always @example.com.

Seeded orders are history: they do not change the product stock.
"""

from __future__ import annotations

import random
import re
from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from faker import Faker
from sqlalchemy.orm import Session

from . import money
from .config import Settings
from .models import (
    Category,
    Coupon,
    CouponUse,
    Order,
    OrderItem,
    Payment,
    Product,
    User,
)
from .reviews import ReviewStore

START = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)

CATEGORIES = [
    ("Testing books", "testing-books"),
    ("Programming books", "programming-books"),
    ("Study gadgets", "study-gadgets"),
]

# sku, name, category slug, price in cents, stock, active, description
PRODUCTS = [
    ("BK-TEST-001", "Testing Basics for Beginners", "testing-books", 1999, 25, True,
     "What testing is, how to write a test case and how to report a bug."),
    ("BK-TEST-002", "API Testing with Python", "testing-books", 2999, 18, True,
     "Send requests, check responses and build a small API test suite."),
    ("BK-TEST-003", "Database Testing Field Guide", "testing-books", 2499, 12, True,
     "Check that the data behind the screen is right, with plain SQL."),
    ("BK-TEST-004", "Playwright Step by Step", "testing-books", 3499, 3, True,
     "Automate a web page from the first click to a full test suite."),
    ("BK-TEST-005", "Exploratory Testing Notebook", "testing-books", 1299, 0, True,
     "A notebook with charters and prompts for exploratory sessions."),
    ("BK-PROG-001", "Python for Testers", "programming-books", 3999, 30, True,
     "The Python you need for test automation, and nothing more."),
    ("BK-PROG-002", "SQL in a Weekend", "programming-books", 1799, 22, True,
     "SELECT, JOIN and GROUP BY, with practice questions."),
    ("BK-PROG-003", "Git and GitHub Basics", "programming-books", 999, 40, True,
     "Save your work, share it and review changes with a team."),
    ("BK-PROG-004", "Docker for Absolute Beginners", "programming-books", 2799, 15, True,
     "Run apps and databases in containers on your own computer."),
    ("GD-001", "Pomodoro Desk Timer", "study-gadgets", 1499, 50, True,
     "A 25-minute timer for focused study sessions."),
    ("GD-002", "Noise-Cancelling Study Headphones", "study-gadgets", 8999, 8, True,
     "Over-ear headphones for quiet study anywhere."),
    ("GD-003", "Bug Hunter Sticky Notes (5 pack)", "study-gadgets", 499, 100, True,
     "Bright sticky notes for test ideas and bug notes."),
    ("GD-004", "Old Model Book Light", "study-gadgets", 1199, 10, False,
     "No longer sold. Hidden from customers."),
]  # fmt: skip

# username, email, full name, role, address
USERS = [
    ("arshad", "arshad@example.com", "Arshad", "customer", "12 Test Street, Sample City"),
    ("maria", "maria@example.com", "Maria Lopez", "customer", "34 Example Road, Demo Town"),
    ("admin", "admin@example.com", "Shop Admin", "admin", None),
]

# code, kind, value, ends at, once per customer
COUPONS = [
    ("WELCOME10", "percent", 10, datetime(2030, 12, 31, 23, 59, tzinfo=UTC), True),
    ("FREESHIP", "free_shipping", 0, datetime(2030, 12, 31, 23, 59, tzinfo=UTC), False),
    ("SPRING25", "percent", 25, datetime(2026, 5, 31, 23, 59, tzinfo=UTC), False),  # ended
]

# customer, [(product sku, quantity)], status, created at, review (rating, text) of the first item
ORDERS = [
    ("arshad", [("BK-TEST-001", 1), ("BK-PROG-003", 2)], "delivered",
     datetime(2026, 2, 10, 14, 30, tzinfo=UTC), (4, "Good start for manual testers.")),
    ("maria", [("BK-TEST-002", 1)], "delivered",
     datetime(2026, 2, 12, 9, 15, tzinfo=UTC), (5, "Clear examples, easy to follow.")),
]  # fmt: skip


def seed(
    session: Session, settings: Settings, hasher: PasswordHasher, reviews: ReviewStore
) -> None:
    categories = {slug: Category(name=name, slug=slug) for name, slug in CATEGORIES}
    session.add_all(categories.values())

    products = {}
    for number, (sku, name, slug, price, stock, active, about) in enumerate(PRODUCTS):
        products[sku] = Product(
            sku=sku,
            name=name,
            description=about,
            category=categories[slug],
            price_cents=price,
            stock=stock,
            is_active=active,
            created_at=START + timedelta(days=4 + number),
        )
    session.add_all(products.values())

    users = {}
    for username, email, full_name, role, address in USERS:
        password = (
            settings.seed_admin_password if role == "admin" else settings.seed_customer_password
        )
        users[username] = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=hasher.hash(password),
            role=role,
            is_verified=True,
            shipping_address=address,
            created_at=START,
        )
    session.add_all(users.values())

    coupons = {
        code: Coupon(code=code, kind=kind, value=value, ends_at=ends_at, once_per_customer=once)
        for code, kind, value, ends_at, once in COUPONS
    }
    session.add_all(coupons.values())
    session.flush()

    review_docs = []
    for username, lines, status, created_at, review in ORDERS:
        user = users[username]
        subtotal = sum(products[sku].price_cents * quantity for sku, quantity in lines)
        totals = money.calculate(subtotal)
        order = Order(
            user_id=user.id,
            status=status,
            shipping_address=user.shipping_address or "",
            created_at=created_at,
            updated_at=created_at + timedelta(days=3),
            **totals.as_dict(),
        )
        order.items = [
            OrderItem(
                product_id=products[sku].id,
                quantity=quantity,
                unit_price_cents=products[sku].price_cents,
            )
            for sku, quantity in lines
        ]
        session.add(order)
        session.flush()
        session.add(
            Payment(
                order_id=order.id,
                card_last4="4242",
                status="succeeded",
                amount_cents=totals.total_cents,
                sandbox_ref=f"sbx_seed_{order.id:04d}",
                created_at=created_at,
            )
        )
        rating, text = review
        review_docs.append(
            {
                "product_id": products[lines[0][0]].id,
                "user_id": user.id,
                "username": user.username,
                "rating": rating,
                "text": text,
                "created_at": created_at + timedelta(days=5),
            }
        )

    if settings.fake_customers > 0:
        review_docs += add_fake_customers(session, settings, hasher, products, coupons)
    session.commit()
    reviews.add_many(review_docs)


# ----- Faker data -----

FAKER_LOCALES = ["en_US", "en_GB", "en_IN", "es_ES"]
LAST_DAY = datetime(2026, 10, 31, 23, 0, tzinfo=UTC)  # fixed, so the data never changes
STATUS_WEIGHTS = {"delivered": 50, "shipped": 15, "paid": 15, "cancelled": 10, "pending": 10}
REVIEW_TEXT = {
    1: ["Not what I expected.", "The pages came loose after a week."],
    2: ["Too basic for me.", "Some examples did not work."],
    3: ["Okay, but a bit long.", "Useful in parts."],
    4: ["Good value.", "Helped me a lot at work.", "Clear and practical."],
    5: ["Excellent, I use it every day.", "The best one I have bought.", "Easy to follow."],
}


def fake_username(fake: Faker, taken: set[str]) -> str:
    base = re.sub(r"[^a-z0-9_]", "", fake.user_name().lower())[:16] or "user"
    base = base if len(base) >= 3 else f"{base}_user"
    name, number = base, 1
    while name in taken:
        number += 1
        name = f"{base}{number}"
    taken.add(name)
    return name


def random_time(rng: random.Random, start: datetime, end: datetime) -> datetime:
    seconds = max(0, int((end - start).total_seconds()))
    return (start + timedelta(seconds=rng.randint(0, seconds))).replace(microsecond=0)


def add_fake_customers(
    session: Session,
    settings: Settings,
    hasher: PasswordHasher,
    products: dict[str, Product],
    coupons: dict[str, Coupon],
) -> list[dict]:
    fake = Faker(FAKER_LOCALES)
    fake.seed_instance(settings.faker_seed)
    rng = random.Random(settings.faker_seed)  # noqa: S311  (fake data, not security)
    taken = {username for username, *_ in USERS}
    for_sale = [product for product in products.values() if product.is_active]
    statuses, weights = list(STATUS_WEIGHTS), list(STATUS_WEIGHTS.values())
    review_docs = []

    for _ in range(settings.fake_customers):
        username = fake_username(fake, taken)
        joined = random_time(rng, START, LAST_DAY - timedelta(days=30))
        user = User(
            username=username,
            email=f"{username}@example.com",
            full_name=fake.name(),
            password_hash=hasher.hash(settings.seed_customer_password),
            role="customer",
            is_verified=rng.random() < 0.9,  # a few never finished signing up
            shipping_address=fake.address().replace("\n", ", ")[:300],
            created_at=joined,
        )
        session.add(user)
        session.flush()
        if not user.is_verified:
            continue

        used_welcome = False
        reviewed: set[int] = set()
        for _ in range(rng.randint(0, 4)):
            created_at = random_time(rng, joined, LAST_DAY)
            status = rng.choices(statuses, weights)[0]
            lines = [(p, rng.randint(1, 3)) for p in rng.sample(for_sale, rng.randint(1, 3))]
            coupon = None
            if not used_welcome and rng.random() < 0.15:
                coupon, used_welcome = coupons["WELCOME10"], True
            elif rng.random() < 0.1:
                coupon = coupons["FREESHIP"]
            subtotal = sum(product.price_cents * quantity for product, quantity in lines)
            totals = money.calculate(subtotal, coupon.kind if coupon else None,
                                     coupon.value if coupon else 0)  # fmt: skip
            moved_days = {"shipped": 2, "delivered": 5, "cancelled": 1}.get(status, 0)
            order = Order(
                user_id=user.id,
                status=status,
                coupon_code=coupon.code if coupon else None,
                shipping_address=user.shipping_address,
                created_at=created_at,
                updated_at=created_at + timedelta(days=moved_days),
                **totals.as_dict(),
            )
            order.items = [
                OrderItem(product_id=p.id, quantity=q, unit_price_cents=p.price_cents)
                for p, q in lines
            ]
            session.add(order)
            session.flush()
            payment_status = {"pending": "declined", "cancelled": "refunded"}.get(
                status, "succeeded"
            )
            session.add(
                Payment(
                    order_id=order.id,
                    card_last4="0002" if payment_status == "declined" else "4242",
                    status=payment_status,
                    amount_cents=totals.total_cents,
                    sandbox_ref=f"sbx_seed_{order.id:04d}",
                    created_at=created_at,
                )
            )
            if coupon is not None and status != "pending":
                session.add(CouponUse(coupon_id=coupon.id, user_id=user.id, order_id=order.id))

            if status != "delivered":
                continue
            for product, _quantity in lines:
                if product.id in reviewed or rng.random() > 0.4:
                    continue
                reviewed.add(product.id)
                rating = rng.choices([1, 2, 3, 4, 5], [1, 1, 3, 6, 8])[0]
                review_docs.append(
                    {
                        "product_id": product.id,
                        "user_id": user.id,
                        "username": user.username,
                        "rating": rating,
                        "text": rng.choice(REVIEW_TEXT[rating]),
                        "created_at": order.updated_at + timedelta(days=rng.randint(1, 20)),
                    }
                )
    return review_docs
