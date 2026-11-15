"""Tester tools: is the app healthy, and which version is it?"""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .. import __version__
from ..deps import AppSettings

router = APIRouter(tags=["Tester tools"])


def database_up(session_maker) -> str:
    try:
        with session_maker() as session:
            session.execute(text("SELECT 1"))
        return "up"
    except SQLAlchemyError:
        return "down"


def health_report(app) -> dict:
    """Every part of the app and whether it is up. Used by /api/health and /status."""
    state = app.state
    services = {
        "api": "up",
        "main_database": database_up(state.sessionmaker),
        "reporting_database": database_up(state.reporting_sessionmaker),
        "reviews_database": "up" if state.reviews.is_up() else "down",
        "email": state.outbox.is_up(),
    }
    ok = all(value in ("up", "console") for value in services.values())
    return {"status": "ok" if ok else "degraded", "services": services}


@router.get("/health", summary="Is every part of the app up?")
def health(request: Request) -> JSONResponse:
    """200 when every part is up, 503 when any part is down.

    `email` is "console" when emails are only printed in the terminal (no SMTP_HOST):
    that counts as up."""
    body = health_report(request.app)
    return JSONResponse(body, status_code=200 if body["status"] == "ok" else 503)


@router.get("/version", summary="Which version of the app is this?")
def version(request: Request, settings: AppSettings) -> dict:
    return {
        "name": "Bookshelf",
        "version": __version__,
        "databases": settings.database_kinds,
        "docs": str(request.url_for("swagger_ui_html")),
    }
