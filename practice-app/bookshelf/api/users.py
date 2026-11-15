"""Your own profile, and the user list for admins."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Response, UploadFile
from fastapi import File as FormFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select

from .. import files
from ..deps import (
    AdminUser,
    AppClock,
    AppSettings,
    CurrentUser,
    Db,
    PageNumber,
    PageSize,
    page_count,
)
from ..errors import ApiError
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


NO_AVATAR = ("AVATAR_NOT_FOUND", "No profile picture.")


@router.post("/me/avatar", response_model=UserOut, summary="Upload my profile picture")
def upload_avatar(
    user: CurrentUser,
    db: Db,
    settings: AppSettings,
    clock: AppClock,
    file: Annotated[UploadFile, FormFile(description="A JPEG or PNG picture, up to 2 MB")],
) -> User:
    """Send the picture as multipart form data in a field named `file`.
    The old picture is replaced."""
    record = files.save_upload(db, settings, user, "avatar", file.file, file.filename, clock.now())
    old = user.avatar_path
    user.avatar_path = record.storage_path
    db.commit()
    files.remove(settings.files_dir, old)
    return user


@router.delete("/me/avatar", status_code=204, summary="Remove my profile picture")
def delete_avatar(user: CurrentUser, db: Db, settings: AppSettings) -> Response:
    if not user.avatar_path:
        raise ApiError(404, *NO_AVATAR)
    old = user.avatar_path
    user.avatar_path = None
    db.commit()
    files.remove(settings.files_dir, old)
    return Response(status_code=204)


def avatar_response(settings, target: User | None) -> FileResponse:
    if target is None or not target.avatar_path:
        raise ApiError(404, *NO_AVATAR)
    path = files.resolve(settings.files_dir, target.avatar_path)
    if not path.is_file():
        raise ApiError(404, *NO_AVATAR)
    return FileResponse(
        path,
        media_type=files.content_type_of(target.avatar_path),
        headers={"Cache-Control": "private, no-store"},
    )


@router.get(
    "/{user_id}/avatar",
    response_class=FileResponse,
    summary="Get a profile picture (your own, or any as admin)",
    responses={200: {"content": {"image/jpeg": {}, "image/png": {}}}},
)
def get_avatar(user_id: int, user: CurrentUser, db: Db, settings: AppSettings) -> FileResponse:
    if user.id != user_id and user.role != "admin":  # someone else's picture looks like none
        raise ApiError(404, *NO_AVATAR)
    return avatar_response(settings, db.get(User, user_id))
