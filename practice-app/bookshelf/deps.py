"""Shared pieces that endpoints ask for: the database session, the clock, and who
is logged in."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .clock import Clock
from .config import Settings
from .errors import ApiError
from .mailer import Outbox
from .models import User
from .security import read_token

bearer = HTTPBearer(
    auto_error=False, description="Paste the access_token from POST /api/auth/login"
)


def get_db(request: Request) -> Iterator[Session]:
    with request.app.state.sessionmaker() as session:
        yield session


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_clock(request: Request) -> Clock:
    return request.app.state.clock


def get_outbox(request: Request) -> Outbox:
    return request.app.state.outbox


def get_hasher(request: Request) -> PasswordHasher:
    return request.app.state.hasher


Db = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]
AppClock = Annotated[Clock, Depends(get_clock)]
AppOutbox = Annotated[Outbox, Depends(get_outbox)]
Hasher = Annotated[PasswordHasher, Depends(get_hasher)]
Credentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]

NOT_LOGGED_IN = {"WWW-Authenticate": "Bearer"}


def optional_user(
    db: Db, settings: AppSettings, clock: AppClock, creds: Credentials
) -> User | None:
    if creds is None:
        return None
    user_id = read_token(settings.secret_key, creds.credentials, clock.now())
    user = db.get(User, user_id) if user_id is not None else None
    if user is None:
        raise ApiError(
            401,
            "INVALID_TOKEN",
            "Your login token is not valid or has expired.",
            headers=NOT_LOGGED_IN,
        )
    return user


def current_user(user: Annotated[User | None, Depends(optional_user)]) -> User:
    if user is None:
        raise ApiError(401, "NOT_AUTHENTICATED", "Log in first.", headers=NOT_LOGGED_IN)
    return user


def admin_user(user: Annotated[User, Depends(current_user)]) -> User:
    if user.role != "admin":
        raise ApiError(403, "FORBIDDEN", "Only an admin can do this.")
    return user


MaybeUser = Annotated[User | None, Depends(optional_user)]
CurrentUser = Annotated[User, Depends(current_user)]
AdminUser = Annotated[User, Depends(admin_user)]

PageNumber = Annotated[int, Query(ge=1, le=100_000, description="Page number, from 1")]
PageSize = Annotated[int, Query(ge=1, le=50, description="Items per page, 1 to 50")]


def page_count(total: int, size: int) -> int:
    return (total + size - 1) // size
