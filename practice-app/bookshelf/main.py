"""Build the app: settings, database, routes, error shapes and request IDs."""

from __future__ import annotations

import re
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from . import __version__, errors
from .api import admin, auth, cart, orders, products, tools, users
from .clock import Clock
from .config import Settings
from .database import prepare
from .db import make_engine, make_sessionmaker
from .mailer import Outbox
from .security import make_hasher

SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

DESCRIPTION = """
**Bookshelf** is the Practice App for [Zero to SDET](https://arshaduzzaman-sm.github.io/zero-to-sdet/):
a small online shop for books and study gadgets.

> For practice on your own computer only. Never deploy it to the internet.

**Try it:** `POST /api/auth/login` with `{"username": "arshad", "password": "Test@1234"}`,
copy the `access_token`, press **Authorize** and paste it.

Every error looks like `{"error": {"code": "...", "message": "...", "request_id": "..."}}`.
Every response has an `X-Request-ID` header.
"""


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    if settings.database_url.startswith("sqlite:///"):
        from pathlib import Path

        Path(settings.database_url.removeprefix("sqlite:///")).parent.mkdir(
            parents=True, exist_ok=True
        )
    app = FastAPI(
        title="Bookshelf Practice App",
        version=__version__,
        description=DESCRIPTION,
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
    )
    app.state.settings = settings
    app.state.engine = make_engine(settings.database_url)
    app.state.sessionmaker = make_sessionmaker(app.state.engine)
    app.state.clock = Clock()
    app.state.outbox = Outbox(settings.outbox_dir)
    app.state.hasher = make_hasher(settings.fast_password_hashing)
    prepare(app)

    errors.install(app)

    @app.middleware("http")
    async def request_id(request: Request, call_next):
        incoming = request.headers.get("X-Request-ID", "")
        request.state.request_id = incoming if SAFE_REQUEST_ID.match(incoming) else uuid.uuid4().hex
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        return response

    for module in (auth, users, products, cart, orders, admin, tools):
        app.include_router(module.router, prefix="/api")

    @app.get("/", include_in_schema=False)
    def home() -> RedirectResponse:
        return RedirectResponse("/docs")  # the web pages come in step 1.5.4

    return app
