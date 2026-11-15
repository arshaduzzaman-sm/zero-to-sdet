"""Shared pieces for the web pages: login cookie, CSRF check, messages, forms."""

from __future__ import annotations

import hmac
import secrets
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError

from .. import __version__
from ..deps import AppClock, AppSettings, Db
from ..errors import ApiError
from ..models import User
from ..security import read_token

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
SESSION_COOKIE = "bookshelf_session"
CSRF_COOKIE = "bookshelf_csrf"

# Short message keys in the address (?msg=added), so no text from outside is ever shown.
MESSAGES = {
    "added": "Added to your cart.",
    "cart_updated": "Your cart is updated.",
    "removed": "Removed from your cart.",
    "coupon_added": "Coupon added.",
    "coupon_removed": "Coupon removed.",
    "logged_in": "Welcome back! You are logged in.",
    "logged_out": "You are logged out.",
    "signed_up": "Account created. We sent a 6-digit code to your email.",
    "code_sent": "If that email has an account, we sent a code to it.",
    "verified": "Your email is verified. You can log in now.",
    "password_changed": "Your password is changed. Log in with the new one.",
    "profile_saved": "Your profile is saved.",
    "ordered": "Thank you! Your order is placed.",
    "cancelled": "Your order is cancelled.",
    "reviewed": "Thank you for your review.",
    "login_needed": "Please log in first.",
    "session_expired": "Your session has ended. Please log in again.",
    "product_saved": "Product saved.",
    "product_created": "Product added.",
    "status_changed": "Order status changed.",
    "reset_done": "All data is back to the start.",
    "synced": "Reporting copy refreshed.",
}


def money(cents: int | None) -> str:
    return "" if cents is None else f"${cents / 100:,.2f}"


def make_templates() -> Jinja2Templates:
    templates = Jinja2Templates(directory=str(TEMPLATES))  # escapes every value by default
    templates.env.filters["money"] = money
    templates.env.globals["app_version"] = __version__
    return templates


def parse_money(text: str) -> int | None:
    """'12.5' -> 1250. Empty -> None. Raises ValueError for anything else."""
    text = text.strip().lstrip("$")
    if not text:
        return None
    try:
        value = Decimal(text)
    except InvalidOperation as error:
        raise ValueError("Enter a price like 12.99.") from error
    if value < 0 or value > 100_000 or value != value.quantize(Decimal("0.01")):
        raise ValueError("Enter a price like 12.99.")
    return int(value * 100)


def safe_next(target: str | None) -> str:
    """Only go back to a page of this site (never to another site after login)."""
    if target and target.startswith("/") and not target.startswith("//") and "\\" not in target:
        return target
    return "/"


def web_user(request: Request, db: Db, settings: AppSettings, clock: AppClock) -> User | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    user_id = read_token(settings.secret_key, token, clock.now())
    return db.get(User, user_id) if user_id is not None else None


WebUser = Annotated[User | None, Depends(web_user)]


class LoginRequired(Exception):  # noqa: N818  (a signal, not an error)
    def __init__(self, next_path: str, expired: bool = False) -> None:
        self.next_path = next_path
        self.expired = expired


class Forbidden(Exception):  # noqa: N818
    pass


class BadCsrf(Exception):  # noqa: N818
    pass


def need_user(request: Request, user: User | None) -> User:
    if user is None:
        raise LoginRequired(request.url.path, expired=SESSION_COOKIE in request.cookies)
    return user


def need_admin(request: Request, user: User | None) -> User:
    user = need_user(request, user)
    if user.role != "admin":
        raise Forbidden()
    return user


async def form_data(request: Request) -> dict[str, str]:
    """Read a submitted form and check its CSRF token (blocks forged form posts)."""
    form = await request.form()
    sent = str(form.get("csrf_token", ""))
    expected = request.cookies.get(CSRF_COOKIE, "")
    if not expected or not hmac.compare_digest(sent, expected):
        raise BadCsrf()
    return {key: str(value) for key, value in form.items() if key != "csrf_token"}


Form = Annotated[dict[str, str], Depends(form_data)]


def csrf_token(request: Request) -> str:
    token = request.cookies.get(CSRF_COOKIE)
    if not token:
        token = getattr(request.state, "new_csrf", None) or secrets.token_urlsafe(32)
        request.state.new_csrf = token
    return token


def secure_cookies(request: Request) -> bool:
    return request.url.scheme == "https"


def render(
    request: Request,
    template: str,
    context: dict[str, Any] | None = None,
    status: int = 200,
    user: User | None = None,
) -> HTMLResponse:
    context = dict(context or {})
    context.setdefault("user", user)
    context.setdefault("message", MESSAGES.get(request.query_params.get("msg", "")))
    context["csrf_token"] = csrf_token(request)
    context["cart_count"] = context.get("cart_count", cart_count(request, user))
    response = request.app.state.templates.TemplateResponse(
        request, template, context, status_code=status
    )
    new = getattr(request.state, "new_csrf", None)
    if new:
        response.set_cookie(
            CSRF_COOKIE, new, httponly=True, samesite="lax", secure=secure_cookies(request)
        )
    return response


def cart_count(request: Request, user: User | None) -> int:
    if user is None:
        return 0
    from ..models import Cart

    with request.app.state.sessionmaker() as session:
        cart = session.query(Cart).filter(Cart.user_id == user.id).first()
        return sum(item.quantity for item in cart.items) if cart else 0


def go(path: str, msg: str | None = None) -> RedirectResponse:
    """Redirect after a form post (so a page refresh never sends the form twice)."""
    target = f"{path}{'&' if '?' in path else '?'}msg={msg}" if msg else path
    return RedirectResponse(target, status_code=303)


def parse(model: type[BaseModel], data: dict[str, Any]) -> tuple[Any, dict[str, str]]:
    """Check form data with the API's own rules. Returns (model or None, errors by field)."""
    try:
        return model(**data), {}
    except ValidationError as error:
        errors: dict[str, str] = {}
        for item in error.errors():
            field = str(item["loc"][0]) if item["loc"] else "form"
            message = str(item["msg"]).removeprefix("Value error, ")
            errors.setdefault(field, message)
        return None, errors


def api_error_text(error: ApiError) -> str:
    return error.message
