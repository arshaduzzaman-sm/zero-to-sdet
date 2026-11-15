"""Shared test setup: a fresh app with its own in-memory database for every test."""

import re

import pytest
from fastapi.testclient import TestClient

from bookshelf.config import Settings
from bookshelf.main import create_app

PASSWORD = "Test@1234"
ADMIN_PASSWORD = "local_only_password"
CARD_OK = "4242 4242 4242 4242"
CARD_DECLINED = "4000 0000 0000 0002"
CARD_TIMEOUT = "4000 0000 0000 9995"


@pytest.fixture
def app():
    settings = Settings(
        database_url="sqlite://",
        secret_key="test-only-secret-key-that-is-long-enough",
        outbox_dir=None,
        fast_password_hashing=True,
        payment_timeout_seconds=0,
    )
    return create_app(settings)


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
