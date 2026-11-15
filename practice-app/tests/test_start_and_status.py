"""Starting safely (the fake-password guard), the reset command, and /status."""

import pytest

from bookshelf import __main__ as start
from bookshelf.config import Settings
from bookshelf.guard import fake_settings, start_problem

from . import conftest


def defaults(**changes) -> Settings:
    settings = Settings(secret_key="local_only_secret_key_change_me_to_any_long_random_text")
    for name, value in changes.items():
        setattr(settings, name, value)
    return settings


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1"])
def test_fake_passwords_are_fine_on_this_computer_only(host):
    assert start_problem(defaults(host=host), {}) is None


def test_fake_passwords_on_an_open_address_stop_the_app():
    problem = start_problem(defaults(host="0.0.0.0"), {})  # noqa: S104  (that is the test)
    assert problem is not None
    assert "SECRET_KEY" in problem and "SEED_ADMIN_PASSWORD" in problem
    assert "HOST=127.0.0.1" in problem


def test_every_fake_value_is_found():
    settings = defaults(
        database_url="postgresql+psycopg://bookshelf:local_only_password@db/bookshelf",
        reporting_database_url="mysql+pymysql://bookshelf:local_only_password@db/reporting",
        mongodb_url="mongodb://bookshelf:local_only_password@db/",
    )
    assert fake_settings(settings) == [
        "SECRET_KEY",
        "SEED_ADMIN_PASSWORD",
        "SEED_CUSTOMER_PASSWORD",
        "DATABASE_URL",
        "REPORTING_DATABASE_URL",
        "MONGODB_URL",
    ]


def test_own_passwords_may_use_an_open_address():
    settings = defaults(
        host="0.0.0.0",  # noqa: S104
        secret_key="a-long-random-text-only-I-know-123456",
        seed_admin_password="my own admin password",  # noqa: S106
        seed_customer_password="my own customer password",  # noqa: S106
    )
    assert start_problem(settings, {}) is None


def test_docker_publishes_on_this_computer_only():
    env = {"CONTAINER_PORT_IS_LOCAL_ONLY": "yes"}
    assert start_problem(defaults(host="0.0.0.0"), env) is None  # noqa: S104


def test_main_refuses_to_start(monkeypatch, capsys):
    monkeypatch.setattr(Settings, "from_env", classmethod(lambda cls: defaults(host="0.0.0.0")))  # noqa: S104
    monkeypatch.delenv("CONTAINER_PORT_IS_LOCAL_ONLY", raising=False)
    started = []
    monkeypatch.setattr(start.uvicorn, "run", lambda *a, **k: started.append(a))
    assert start.main([]) == 1
    assert "Refusing to start" in capsys.readouterr().err
    assert started == []


def test_reset_command_brings_back_the_seed_data(monkeypatch, capsys, tmp_path):
    database = tmp_path / "main.db"
    settings = conftest.test_settings(
        database_url=f"sqlite:///{database}",
        reporting_database_url=f"sqlite:///{tmp_path / 'r.db'}",
    )
    if settings.mongodb_url:
        pytest.skip("uses its own SQLite files")
    monkeypatch.setattr(Settings, "from_env", classmethod(lambda cls: settings))
    assert start.main(["reset"]) == 0
    assert "back to the seed data" in capsys.readouterr().out
    assert database.exists()


def test_unknown_command(capsys):
    assert start.main(["delete-everything"]) == 2
    assert "Usage" in capsys.readouterr().err


def test_status_page_shows_every_part(client):
    page = client.get("/status")
    assert page.status_code == 200
    assert 'data-testid="status-summary">Every part of the app is working.' in page.text
    assert page.text.count('data-testid="status-row"') == 5
    assert 'data-service="email"' in page.text


def test_status_page_says_when_a_part_is_down(client, app, monkeypatch):
    monkeypatch.setattr(app.state.reviews, "is_up", lambda: False)
    page = client.get("/status")
    assert page.status_code == 503
    assert "Some parts are down" in page.text
    assert client.get("/api/health").json()["services"]["reviews_database"] == "down"
