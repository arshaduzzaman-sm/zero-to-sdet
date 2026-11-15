"""Stops the app from starting where other computers could reach it while it
still uses the fake passwords from .env.example.

On 127.0.0.1 (the default) only your own computer can reach the app, so the
fake passwords are fine. On any other address (for example 0.0.0.0), anyone on
the same network could log in as admin with `local_only_password`.

Docker is the one exception: inside a container the app must listen on 0.0.0.0,
but docker-compose.yml publishes its port on 127.0.0.1 only and says so with
CONTAINER_PORT_IS_LOCAL_ONLY=yes.
"""

from __future__ import annotations

from .config import Settings

LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
FAKE_CUSTOMER_PASSWORD = "Test@1234"  # noqa: S105  (the known fake one)


def fake_settings(settings: Settings) -> list[str]:
    """Names of the settings that still hold a fake, publicly known value."""
    found = []
    if "local_only" in settings.secret_key:
        found.append("SECRET_KEY")
    if "local_only" in settings.seed_admin_password:
        found.append("SEED_ADMIN_PASSWORD")
    if settings.seed_customer_password == FAKE_CUSTOMER_PASSWORD:
        found.append("SEED_CUSTOMER_PASSWORD")
    urls = {
        "DATABASE_URL": settings.database_url,
        "REPORTING_DATABASE_URL": settings.reporting_database_url,
        "MONGODB_URL": settings.mongodb_url,
    }
    found += [name for name, url in urls.items() if "local_only" in url]
    return found


def start_problem(settings: Settings, env: dict[str, str]) -> str | None:
    """None when it is safe to start; otherwise the message that explains why not."""
    if settings.host in LOCAL_HOSTS:
        return None
    if env.get("CONTAINER_PORT_IS_LOCAL_ONLY", "").lower() == "yes":
        return None
    fakes = fake_settings(settings)
    if not fakes:
        return None
    return (
        f"Refusing to start on {settings.host}: other computers could reach the app, and "
        f"these settings still use the fake values from .env.example: {', '.join(fakes)}.\n"
        "Use HOST=127.0.0.1 (recommended), or change those values in practice-app/.env first."
    )
