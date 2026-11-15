"""Totals math (bookshelf/money.py): tax, shipping and coupons, at the edges."""

import pytest

from bookshelf.money import calculate, percent_of


@pytest.mark.parametrize(("amount", "expected"), [
    (1994, 199),  # 199.4 rounds down
    (1995, 200),  # 199.5 rounds half up
    (1999, 200),
    (0, 0),
])  # fmt: skip
def test_ten_percent_rounds_half_up(amount, expected):
    assert percent_of(amount, 10) == expected


@pytest.mark.parametrize(("subtotal", "shipping"), [
    (0, 0),        # empty cart: no shipping
    (4999, 499),   # 49.99: just under the free shipping line
    (5000, 0),     # 50.00: free
    (5001, 0),
])  # fmt: skip
def test_free_shipping_from_50(subtotal, shipping):
    assert calculate(subtotal).shipping_cents == shipping


def test_total_adds_up():
    totals = calculate(3997)
    assert totals.tax_cents == 400
    assert totals.total_cents == 3997 + 400 + 499


def test_percent_coupon_counts_before_tax_and_shipping():
    totals = calculate(5400, "percent", 10)  # 54.00 - 5.40 = 48.60: under 50, so shipping
    assert totals.discount_cents == 540
    assert totals.tax_cents == 486
    assert totals.shipping_cents == 499
    assert totals.total_cents == 5400 - 540 + 486 + 499


def test_free_shipping_coupon():
    assert calculate(1000, "free_shipping").shipping_cents == 0
