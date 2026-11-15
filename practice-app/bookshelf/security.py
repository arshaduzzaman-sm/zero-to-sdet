"""Passwords, login tokens and one-time codes.

- Passwords are stored as Argon2 hashes, never as plain text.
- Login tokens are JWTs signed with SECRET_KEY. Their expiry is checked against
  the app clock (clock.py), so moving the clock can expire a token in a lesson.
- One-time codes (OTP) are 6 digits, stored as an HMAC, valid 10 minutes, used once,
  and burned after 5 wrong tries.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

OTP_MINUTES = 10
OTP_MAX_ATTEMPTS = 5
ALGORITHM = "HS256"


def make_hasher(fast: bool = False) -> PasswordHasher:
    if fast:  # tests only
        return PasswordHasher(time_cost=1, memory_cost=1024, parallelism=1)
    return PasswordHasher()


_DUMMY_HASHES: dict[int, str] = {}


def dummy_hash(hasher: PasswordHasher) -> str:
    """A hash to check against when the user does not exist, so a wrong username
    takes as long as a wrong password (nobody can time it to find real usernames)."""
    key = id(hasher)
    if key not in _DUMMY_HASHES:
        _DUMMY_HASHES[key] = hasher.hash(secrets.token_urlsafe(16))
    return _DUMMY_HASHES[key]


def verify_password(hasher: PasswordHasher, password_hash: str, password: str) -> bool:
    try:
        return hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError):
        return False


def create_token(secret: str, user_id: int, role: str, now: datetime, minutes: int) -> str:
    claims = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    return jwt.encode(claims, secret, algorithm=ALGORITHM)


def read_token(secret: str, token: str, now: datetime) -> int | None:
    """The user id inside a valid, unexpired token; None for anything else."""
    try:
        claims = jwt.decode(
            token,
            secret,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"], "verify_exp": False, "verify_iat": False},
        )
        if int(claims["exp"]) <= now.timestamp():
            return None
        return int(claims["sub"])
    except (jwt.PyJWTError, ValueError, TypeError):
        return None


def new_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(secret: str, user_id: int, code: str) -> str:
    message = f"{user_id}:{code}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def otp_matches(secret: str, user_id: int, code: str, code_hash: str) -> bool:
    return hmac.compare_digest(hash_otp(secret, user_id, code), code_hash)
