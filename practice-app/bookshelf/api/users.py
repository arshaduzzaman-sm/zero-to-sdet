"""Your own profile, and the user list for admins."""

from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import func, select

from ..deps import AdminUser, CurrentUser, Db, PageNumber, PageSize, page_count
from ..models import User
from ..schemas import Page, UserOut, UserUpdateIn

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut, summary="See my profile")
def my_profile(user: CurrentUser) -> User:
    return user


@router.patch("/me", response_model=UserOut, summary="Change my name or shipping address")
def update_profile(body: UserUpdateIn, user: CurrentUser, db: Db) -> User:
    if body.full_name is not None:
        user.full_name = body.full_name.strip() or user.full_name
    if body.shipping_address is not None:
        user.shipping_address = body.shipping_address.strip() or None
    db.commit()
    return user


@router.get("", response_model=Page[UserOut], summary="List every user (admin)")
def list_users(_admin: AdminUser, db: Db, page: PageNumber = 1, size: PageSize = 20) -> dict:
    total = db.scalar(select(func.count(User.id))) or 0
    users = db.scalars(select(User).order_by(User.id).offset((page - 1) * size).limit(size)).all()
    pages = page_count(total, size)
    return {"items": users, "page": page, "size": size, "total": total, "pages": pages}
