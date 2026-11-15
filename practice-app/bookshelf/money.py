"""Cart and order totals. All amounts are whole cents.

    subtotal  = sum of price x quantity
    discount  = coupon percent of the subtotal (WELCOME10: 10%)
    tax       = 10% of (subtotal - discount)
    shipping  = 0 when (subtotal - discount) is 50.00 or more, otherwise 4.99
                (FREESHIP makes it 0 always; an empty cart has no shipping)
    total     = subtotal - discount + tax + shipping

Percentages round half up to the nearest cent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

TAX_PERCENT = 10
FREE_SHIPPING_FROM_CENTS = 5000
SHIPPING_CENTS = 499


def percent_of(amount_cents: int, percent: int) -> int:
    return (amount_cents * percent + 50) // 100


@dataclass(frozen=True)
class Totals:
    subtotal_cents: int
    discount_cents: int
    tax_cents: int
    shipping_cents: int
    total_cents: int

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


def calculate(subtotal_cents: int, coupon_kind: str | None = None, coupon_value: int = 0) -> Totals:
    discount = percent_of(subtotal_cents, coupon_value) if coupon_kind == "percent" else 0
    after_discount = subtotal_cents - discount
    tax = percent_of(after_discount, TAX_PERCENT)
    if subtotal_cents == 0 or coupon_kind == "free_shipping":
        shipping = 0
    else:
        shipping = 0 if after_discount >= FREE_SHIPPING_FROM_CENTS else SHIPPING_CENTS
    return Totals(subtotal_cents, discount, tax, shipping, after_discount + tax + shipping)
