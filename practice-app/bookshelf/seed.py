"""The starting data. It is the same on every start and after every reset, so
lessons can say "log in as arshad" or "product 4 has only 3 left".

All of it is fake. Step 1.5.3 adds more customers and orders made with Faker
(with a fixed random seed, so they are the same every time too).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from . import money
from .config import Settings
from .models import (
    Category,
    Coupon,
    Order,
    OrderItem,
    Payment,
    Product,
    Review,
    User,
)

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


def seed(session: Session, settings: Settings, hasher: PasswordHasher) -> None:
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

    for code, kind, value, ends_at, once in COUPONS:
        session.add(
            Coupon(code=code, kind=kind, value=value, ends_at=ends_at, once_per_customer=once)
        )
    session.flush()

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
        session.add(
            Review(
                product_id=products[lines[0][0]].id,
                user_id=user.id,
                username=user.username,
                rating=rating,
                text=text,
                created_at=created_at + timedelta(days=5),
            )
        )
    session.commit()
