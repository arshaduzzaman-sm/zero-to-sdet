"""Errors on web pages: a friendly HTML page instead of JSON."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response

from ..security import read_token
from .helpers import SESSION_COOKIE, BadCsrf, Forbidden, LoginRequired, render
from .routes import login_redirect

API_PREFIXES = ("/api", "/docs", "/openapi.json", "/static")

TITLES = {
    400: "Something is not right",
    403: "Not allowed",
    404: "Page not found",
    405: "Not allowed",
    500: "Something went wrong",
}


def is_web(request: Request) -> bool:
    return not request.url.path.startswith(API_PREFIXES)


def cookie_user(request: Request):
    """Who is logged in, for the header of an error page (None if nobody)."""
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    state = request.app.state
    user_id = read_token(state.settings.secret_key, token, state.clock.now())
    if user_id is None:
        return None
    from ..models import User

    with state.sessionmaker() as session:
        return session.get(User, user_id)


def error_page(request: Request, status: int, text: str) -> HTMLResponse:
    return render(
        request,
        "error.html",
        {
            "status": status,
            "title": TITLES.get(status, "Something is not right"),
            "text": text,
            "request_id": getattr(request.state, "request_id", None),
        },
        status=status,
        user=cookie_user(request),
    )


def install(app: FastAPI) -> None:
    app.state.render_error = error_page

    @app.exception_handler(LoginRequired)
    async def _login(request: Request, exc: LoginRequired) -> Response:
        return login_redirect(exc.next_path, exc.expired)

    @app.exception_handler(Forbidden)
    async def _forbidden(request: Request, exc: Forbidden) -> Response:
        return error_page(request, 403, "Only an admin can open this page.")

    @app.exception_handler(BadCsrf)
    async def _csrf(request: Request, exc: BadCsrf) -> Response:
        return error_page(
            request, 403, "This form has expired. Go back, reload the page and try again."
        )
