"""The Faker seed data: realistic, valid, and the same on every run."""

import re

from sqlalchemy import func, select

from bookshelf.models import Order, User
from bookshelf.money import calculate

from .conftest import make_app

USERNAME = re.compile(r"^[a-z0-9_]{3,20}$")


def snapshot(app):
    with app.state.sessionmaker() as session:
        users = session.execute(select(User.username, User.email, User.full_name)).all()
        orders = session.execute(
            select(Order.user_id, Order.status, Order.total_cents).order_by(Order.id)
        ).all()
    return users, orders


def test_faker_data_is_the_same_every_time():
    first = snapshot(make_app(fake_customers=10))
    second = snapshot(make_app(fake_customers=10))
    assert first == second


def test_faker_customers_are_valid_and_fake():
    app = make_app(fake_customers=15)
    with app.state.sessionmaker() as session:
        users = session.scalars(select(User).where(User.id > 3)).all()
        assert len(users) == 15
        for user in users:
            assert USERNAME.match(user.username), user.username
            assert user.email == f"{user.username}@example.com"
            assert user.role == "customer"
        assert session.scalar(select(func.count(User.id)).where(User.is_verified.is_(False)))


def test_faker_orders_add_up():
    app = make_app(fake_customers=15)
    with app.state.sessionmaker() as session:
        orders = session.scalars(select(Order).where(Order.id > 2)).all()
        assert orders, "Faker customers should have orders"
        statuses = {order.status for order in orders}
        assert statuses <= {"pending", "paid", "shipped", "delivered", "cancelled"}
        for order in orders:
            subtotal = sum(item.unit_price_cents * item.quantity for item in order.items)
            assert order.subtotal_cents == subtotal
            assert order.total_cents == (
                subtotal - order.discount_cents + order.tax_cents + order.shipping_cents
            )
            if order.coupon_code is None:
                assert order.total_cents == calculate(subtotal).total_cents


def test_faker_reviews_are_from_buyers():
    app = make_app(fake_customers=15)
    reviews = app.state.reviews
    with app.state.sessionmaker() as session:
        for product_id in range(1, 13):
            for review in reviews.list_for(product_id):
                bought = session.scalar(
                    select(func.count(Order.id)).where(
                        Order.user_id == review["user_id"], Order.status == "delivered"
                    )
                )
                assert bought, review
                assert 1 <= review["rating"] <= 5
