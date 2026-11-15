"""The app's clock. Admins can move it (POST /api/admin/clock) to test time rules
such as OTP expiry, login lockout and coupon end dates without waiting.

The clock keeps ticking after a change: it adds a fixed offset to the real time.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


class Clock:
    def __init__(self) -> None:
        self.offset = timedelta(0)

    def now(self) -> datetime:
        return datetime.now(UTC) + self.offset

    def set(self, when: datetime) -> None:
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        self.offset = when - datetime.now(UTC)

    def advance(self, seconds: int) -> None:
        self.offset += timedelta(seconds=seconds)

    def reset(self) -> None:
        self.offset = timedelta(0)

    @property
    def is_real(self) -> bool:
        return self.offset == timedelta(0)
