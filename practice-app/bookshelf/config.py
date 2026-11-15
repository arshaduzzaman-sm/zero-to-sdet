"""Settings, read from environment variables.

`practice-app/.env` is read too when it exists (copy `.env.example` to start).
Real environment variables win over the file. Nothing here is a real secret:
the app runs on your own computer only.
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent  # practice-app/
DATA_DIR = APP_DIR / "data"  # local database file and emails (ignored by git)


def read_env_file(path: Path) -> dict[str, str]:
    """KEY=VALUE lines; blank lines and # comments are skipped."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


@dataclass
class Settings:
    # Main database. Without Docker: a SQLite file. With Docker: PostgreSQL.
    database_url: str = f"sqlite:///{DATA_DIR / 'bookshelf.db'}"
    # Reporting copy (order_facts, daily_sales). Without Docker: a second SQLite file.
    reporting_database_url: str = f"sqlite:///{DATA_DIR / 'reporting.db'}"
    # Reviews. Empty: a `reviews` table in the main database. With Docker: MongoDB.
    mongodb_url: str = ""
    mongodb_database: str = "bookshelf"
    # How often the reporting copy is refreshed, in seconds (0: only when an admin asks).
    reporting_sync_seconds: int = 60
    # Extra Faker customers (each with a few orders and reviews) in the seed data.
    fake_customers: int = 40
    faker_seed: int = 2026
    # Signs login tokens and OTP codes. Random on every start unless set in .env.
    secret_key: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    token_minutes: int = 30
    host: str = "127.0.0.1"
    port: int = 8080
    # Fake passwords for the seeded users (DESIGN.md section 1).
    seed_customer_password: str = "Test@1234"  # noqa: S105  (fake, local only)
    seed_admin_password: str = "local_only_password"  # noqa: S105  (fake, local only)
    # How long the "timeout" sandbox card waits before it gives up.
    payment_timeout_seconds: float = 3.0
    # Admin clock control (POST /api/admin/clock), for lessons about time.
    clock_control: bool = True
    # Email. With SMTP_HOST set (Mailpit), emails go there and show at http://127.0.0.1:58025.
    # Without it, they are printed in the terminal and saved as text files here.
    smtp_host: str = ""
    smtp_port: int = 1025
    mail_from: str = "Bookshelf <no-reply@bookshelf.example>"
    outbox_dir: Path | None = DATA_DIR / "outbox"
    # Uploaded pictures (profile pictures, product images).
    files_dir: Path = DATA_DIR / "files"
    max_upload_bytes: int = 2 * 1024 * 1024
    # Bug Hunt bugs (bugs.py). PRACTICE_APP_BUGS=off turns them all off.
    planted_bugs: bool = True
    # Tests only: cheaper password hashing so the test run stays fast.
    fast_password_hashing: bool = False

    @classmethod
    def from_env(cls) -> Settings:
        env = {**read_env_file(APP_DIR / ".env"), **os.environ}
        settings = cls()
        text = {
            "DATABASE_URL": "database_url",
            "REPORTING_DATABASE_URL": "reporting_database_url",
            "MONGODB_URL": "mongodb_url",
            "MONGODB_DATABASE": "mongodb_database",
            "SMTP_HOST": "smtp_host",
            "MAIL_FROM": "mail_from",
            "SECRET_KEY": "secret_key",
            "HOST": "host",
            "SEED_CUSTOMER_PASSWORD": "seed_customer_password",
            "SEED_ADMIN_PASSWORD": "seed_admin_password",
        }
        for key, name in text.items():
            if env.get(key):
                setattr(settings, name, env[key])
        for key, name in (
            ("REPORTING_SYNC_SECONDS", "reporting_sync_seconds"),
            ("FAKE_CUSTOMERS", "fake_customers"),
            ("SMTP_PORT", "smtp_port"),
        ):
            if env.get(key):
                setattr(settings, name, int(env[key]))
        if env.get("FILES_DIR"):
            settings.files_dir = Path(env["FILES_DIR"])
        if env.get("PORT"):
            settings.port = int(env["PORT"])
        if env.get("TOKEN_MINUTES"):
            settings.token_minutes = int(env["TOKEN_MINUTES"])
        if env.get("PAYMENT_TIMEOUT_SECONDS"):
            settings.payment_timeout_seconds = float(env["PAYMENT_TIMEOUT_SECONDS"])
        if env.get("PRACTICE_APP_BUGS"):
            settings.planted_bugs = env["PRACTICE_APP_BUGS"].lower() not in (
                "0",
                "off",
                "false",
                "no",
            )
        if env.get("CLOCK_CONTROL"):
            settings.clock_control = env["CLOCK_CONTROL"].lower() in ("1", "on", "true", "yes")
        return settings

    @property
    def database_kinds(self) -> dict[str, str]:
        """Which database does each job, e.g. {"main": "postgresql", ...}."""

        def kind(url: str) -> str:
            return url.split(":", 1)[0].split("+", 1)[0]

        return {
            "main": kind(self.database_url),
            "reporting": kind(self.reporting_database_url),
            "reviews": "mongodb" if self.mongodb_url else kind(self.database_url),
        }
