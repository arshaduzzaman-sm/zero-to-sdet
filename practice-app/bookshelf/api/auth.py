"""Sign up, verify the email, log in, reset a forgotten password."""

from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .. import bugs
from ..deps import AppClock, AppOutbox, AppSettings, CurrentUser, Db, Hasher
from ..errors import ApiError
from ..models import OtpCode, User
from ..schemas import (
    EmailIn,
    LoginIn,
    Message,
    ResetPasswordIn,
    SignupIn,
    TokenOut,
    UserOut,
    VerifyIn,
)
from ..security import (
    OTP_MAX_ATTEMPTS,
    OTP_MINUTES,
    create_token,
    dummy_hash,
    hash_otp,
    new_otp,
    otp_matches,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

MAX_FAILED_LOGINS = 5
LOCK_MINUTES = 15
CODE_SENT = "If that email has an account, we sent a code to it."


def issue_code(db: Session, user: User, purpose: str, secret: str, now: datetime) -> str:
    """Make a new code. Older unused codes for the same purpose stop working."""
    for old in db.scalars(
        select(OtpCode).where(
            OtpCode.user_id == user.id, OtpCode.purpose == purpose, OtpCode.used_at.is_(None)
        )
    ):
        old.used_at = now
    code = new_otp()
    db.add(
        OtpCode(
            user_id=user.id,
            code_hash=hash_otp(secret, user.id, code),
            purpose=purpose,
            expires_at=now + timedelta(minutes=OTP_MINUTES),
            created_at=now,
        )
    )
    return code


def use_code(db: Session, user: User | None, purpose: str, code: str, secret: str, now: datetime):
    """Accept the code once, or raise INVALID_CODE / CODE_EXPIRED."""
    invalid = ApiError(400, "INVALID_CODE", "That code is not right. Check the email again.")
    if user is None:
        raise invalid
    otp = db.scalars(
        select(OtpCode)
        .where(OtpCode.user_id == user.id, OtpCode.purpose == purpose, OtpCode.used_at.is_(None))
        .order_by(OtpCode.id.desc())
    ).first()
    if otp is None:
        raise invalid
    if otp.expires_at <= now and not (purpose == "reset" and bugs.on("BH-06")):
        raise ApiError(400, "CODE_EXPIRED", "That code has expired. Ask for a new one.")
    if not otp_matches(secret, user.id, code, otp.code_hash):
        otp.attempts += 1
        if otp.attempts >= OTP_MAX_ATTEMPTS:
            otp.used_at = now  # too many wrong tries: this code is burned
        db.commit()
        raise invalid
    otp.used_at = now


def send_code(outbox, user: User, purpose: str, code: str, now: datetime) -> None:
    if purpose == "verify":
        subject, action = "Your Bookshelf sign-up code", "finish signing up"
    else:
        subject, action = "Your Bookshelf password reset code", "set a new password"
    body = (
        f"Hello {user.full_name},\n\nYour code is {code}. Use it to {action}.\n"
        f"It works once and expires in {OTP_MINUTES} minutes."
    )
    outbox.send(user.email, subject, body, now)


def find_user(db: Session, username_or_email: str) -> User | None:
    value = username_or_email.strip().lower()
    return db.scalars(select(User).where(or_(User.username == value, User.email == value))).first()


@router.post("/signup", status_code=201, response_model=UserOut, summary="Create an account")
def signup(
    body: SignupIn,
    db: Db,
    settings: AppSettings,
    clock: AppClock,
    outbox: AppOutbox,
    hasher: Hasher,
) -> User:
    """Creates an unverified account and emails a 6-digit code (see POST /auth/verify)."""
    if db.scalars(select(User).where(User.email == body.email)).first():
        raise ApiError(409, "EMAIL_TAKEN", "An account with this email already exists.")
    if db.scalars(select(User).where(User.username == body.username)).first():
        raise ApiError(409, "USERNAME_TAKEN", "This username is taken. Try another one.")
    now = clock.now()
    user = User(
        username=body.username,
        email=body.email,
        full_name=body.full_name,
        password_hash=hasher.hash(body.password),
        role="customer",
        is_verified=False,
        created_at=now,
    )
    db.add(user)
    db.flush()
    code = issue_code(db, user, "verify", settings.secret_key, now)
    db.commit()
    send_code(outbox, user, "verify", code, now)
    return user


@router.post("/verify", response_model=Message, summary="Confirm the email with the code")
def verify(body: VerifyIn, db: Db, settings: AppSettings, clock: AppClock) -> Message:
    user = db.scalars(select(User).where(User.email == body.email)).first()
    if user is not None and user.is_verified:
        raise ApiError(409, "ALREADY_VERIFIED", "This account is already verified. Log in.")
    use_code(db, user, "verify", body.code, settings.secret_key, clock.now())
    user.is_verified = True
    db.commit()
    return Message(message="Your email is verified. You can log in now.")


@router.post(
    "/resend-code", status_code=202, response_model=Message, summary="Send a new sign-up code"
)
def resend_code(
    body: EmailIn, db: Db, settings: AppSettings, clock: AppClock, outbox: AppOutbox
) -> Message:
    user = db.scalars(select(User).where(User.email == body.email)).first()
    if user is not None and not user.is_verified:
        now = clock.now()
        code = issue_code(db, user, "verify", settings.secret_key, now)
        db.commit()
        send_code(outbox, user, "verify", code, now)
    return Message(message=CODE_SENT)


@router.post("/login", response_model=TokenOut, summary="Log in and get a bearer token")
def login(
    body: LoginIn, db: Db, settings: AppSettings, clock: AppClock, hasher: Hasher
) -> TokenOut:
    """Log in with your username (or email) and password.

    Five wrong passwords in a row lock the account for 15 minutes.
    """
    wrong = ApiError(401, "INVALID_CREDENTIALS", "The username or password is not right.")
    now = clock.now()
    user = find_user(db, body.username)
    if user is None:
        verify_password(hasher, dummy_hash(hasher), body.password)  # same time as a real check
        raise wrong
    if user.locked_until is not None and user.locked_until > now:
        minutes = max(1, int((user.locked_until - now).total_seconds() // 60) + 1)
        raise ApiError(
            423,
            "ACCOUNT_LOCKED",
            f"Too many wrong passwords. Try again in {minutes} minutes, or reset your password.",
        )
    if not verify_password(hasher, user.password_hash, body.password):
        user.failed_logins += 1
        if user.failed_logins >= MAX_FAILED_LOGINS:
            user.failed_logins = 0
            user.locked_until = now + timedelta(minutes=LOCK_MINUTES)
            db.commit()
            raise ApiError(
                423,
                "ACCOUNT_LOCKED",
                f"Too many wrong passwords. Try again in {LOCK_MINUTES} minutes, "
                "or reset your password.",
            )
        db.commit()
        raise wrong
    if not user.is_verified:
        raise ApiError(403, "EMAIL_NOT_VERIFIED", "Verify your email first (check for the code).")
    user.failed_logins = 0
    user.locked_until = None
    if hasher.check_needs_rehash(user.password_hash):
        user.password_hash = hasher.hash(body.password)
    db.commit()
    token = create_token(settings.secret_key, user.id, user.role, now, settings.token_minutes)
    return TokenOut(access_token=token, expires_in=settings.token_minutes * 60)


@router.post(
    "/forgot-password", status_code=202, response_model=Message, summary="Email a reset code"
)
def forgot_password(
    body: EmailIn, db: Db, settings: AppSettings, clock: AppClock, outbox: AppOutbox
) -> Message:
    """Always gives the same answer, so nobody can use it to find out who has an account."""
    user = db.scalars(select(User).where(User.email == body.email)).first()
    if user is not None:
        now = clock.now()
        code = issue_code(db, user, "reset", settings.secret_key, now)
        db.commit()
        send_code(outbox, user, "reset", code, now)
    return Message(message=CODE_SENT)


@router.post("/reset-password", response_model=Message, summary="Set a new password with the code")
def reset_password(
    body: ResetPasswordIn, db: Db, settings: AppSettings, clock: AppClock, hasher: Hasher
) -> Message:
    user = db.scalars(select(User).where(User.email == body.email)).first()
    use_code(db, user, "reset", body.code, settings.secret_key, clock.now())
    user.password_hash = hasher.hash(body.new_password)
    user.is_verified = True  # the code proves they own the email
    user.failed_logins = 0
    user.locked_until = None
    db.commit()
    return Message(message="Your password is changed. Log in with the new one.")


@router.get("/me", response_model=UserOut, summary="Who am I?")
def me(user: CurrentUser) -> User:
    return user
