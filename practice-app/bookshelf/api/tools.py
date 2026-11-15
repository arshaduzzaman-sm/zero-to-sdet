"""Tester tools: is the app healthy, and which version is it?"""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .. import __version__
from ..deps import AppSettings, Db

router = APIRouter(tags=["Tester tools"])


@router.get("/health", summary="Is every part of the app up?")
def health(db: Db, settings: AppSettings) -> JSONResponse:
    """200 when every part is up, 503 when any part is down. Step 1.5.6 adds the
    other services (MySQL, MongoDB, Mailpit)."""
    try:
        db.execute(text("SELECT 1"))
        database = "up"
    except Exception:  # noqa: BLE001  (any failure means "down")
        database = "down"
    services = {"api": "up", "database": database}
    ok = all(state == "up" for state in services.values())
    body = {"status": "ok" if ok else "degraded", "services": services}
    return JSONResponse(body, status_code=200 if ok else 503)


@router.get("/version", summary="Which version of the app is this?")
def version(request: Request, settings: AppSettings) -> dict:
    return {
        "name": "Bookshelf",
        "version": __version__,
        "database": settings.database_kind,
        "docs": str(request.url_for("swagger_ui_html")),
    }
