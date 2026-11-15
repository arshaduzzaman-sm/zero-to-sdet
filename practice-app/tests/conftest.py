"""Shared test setup: a fresh app with fresh data for every test.

By default every test gets its own in-memory SQLite databases (fast, no Docker).
To run the same tests against the Docker databases (docker compose up -d), set:

    BOOKSHELF_TEST_DATABASE_URL     e.g. postgresql+psycopg://bookshelf:...@127.0.0.1:55432/bookshelf
    BOOKSHELF_TEST_REPORTING_URL    e.g. mysql+pymysql://bookshelf:...@127.0.0.1:53306/reporting
    BOOKSHELF_TEST_MONGODB_URL      e.g. mongodb://bookshelf:...@127.0.0.1:57017/?authSource=admin

Careful: each test resets those databases, so local practice data is lost.
"""

import os
import re

import pytest
from fastapi.testclient import TestClient

from bookshelf.config import Settings
from bookshelf.database import reset_data
from bookshelf.main import create_app

DATABASE_URL = os.environ.get("BOOKSHELF_TEST_DATABASE_URL", "")
REPORTING_URL = os.environ.get("BOOKSHELF_TEST_REPORTING_URL", "")
MONGODB_URL = os.environ.get("BOOKSHELF_TEST_MONGODB_URL", "")

PASSWORD = "Test@1234"
ADMIN_PASSWORD = "local_only_password"
CARD_OK = "4242 4242 4242 4242"
CARD_DECLINED = "4000 0000 0000 0002"
CARD_TIMEOUT = "4000 0000 0000 9995"


def test_settings(**changes) -> Settings:
    settings = Settings(
        database_url=DATABASE_URL or "sqlite://",
        reporting_database_url=REPORTING_URL or "sqlite://",
        mongodb_url=MONGODB_URL,
        mongodb_database="bookshelf_test",
        secret_key="test-only-secret-key-that-is-long-enough",
        outbox_dir=None,
        fast_password_hashing=True,
        payment_timeout_seconds=0,
        reporting_sync_seconds=0,
        fake_customers=0,  # tests use only the fixed seed data, so numbers stay small
    )
    for name, value in changes.items():
        setattr(settings, name, value)
    return settings


def make_app(**changes):
    app = create_app(test_settings(**changes))
    if DATABASE_URL or REPORTING_URL or MONGODB_URL:
        reset_data(app)  # shared databases: start every test from the seed data
    return app


@pytest.fixture
def app():
    return make_app()


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def outbox(app):
    return app.state.outbox


@pytest.fixture
def clock(app):
    return app.state.clock


@pytest.fixture
def login(client):
    """login("arshad") -> headers with a bearer token."""

    def _login(username: str = "arshad", password: str | None = None) -> dict:
        if password is None:
            password = ADMIN_PASSWORD if username == "admin" else PASSWORD
        response = client.post("/api/auth/login", json={"username": username, "password": password})
        assert response.status_code == 200, response.text
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    return _login


def code_in(email) -> str:
    """The 6-digit code inside an email."""
    match = re.search(r"\b(\d{6})\b", email.body)
    assert match, email.body
    return match.group(1)


def error_code(response) -> str:
    return response.json()["error"]["code"]


def checkout(client, headers, card=CARD_OK, **extra):
    body = {"card_number": card, "expiry": "12/30", "cvc": "123", **extra}
    return client.post("/api/checkout", json=body, headers=headers)
