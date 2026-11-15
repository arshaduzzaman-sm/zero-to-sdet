"""Uploaded pictures: profile pictures and product images.

Uploads are never trusted:
- At most MAX_UPLOAD_BYTES (2 MB); bigger files are refused.
- Pillow must open the file as a real JPEG or PNG. The name and the browser's
  "content type" are ignored: a renamed .txt or .exe is refused.
- Very large pictures (more than 25 million pixels) are refused before decoding.
- A clean copy is saved: rotated upright, re-encoded, with no hidden metadata
  (for example the GPS location a phone camera adds).
- The file gets a random name in practice-app/data/files/. The uploaded file
  name is kept only as text in the database, never used as a path.
"""

from __future__ import annotations

import hashlib
import io
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from .errors import ApiError
from .models import File

MAX_PIXELS = 25_000_000
FORMATS = {"JPEG": ("jpg", "image/jpeg"), "PNG": ("png", "image/png")}
FOLDERS = {"avatar": "avatars", "product_image": "product-images"}


@dataclass
class CleanImage:
    data: bytes
    extension: str
    content_type: str
    sha256: str


def read_limited(stream, limit: int) -> bytes:
    """Read at most `limit` bytes; refuse anything bigger."""
    data = stream.read(limit + 1)
    if len(data) > limit:
        raise ApiError(
            413, "FILE_TOO_LARGE", f"The file is bigger than {limit // (1024 * 1024)} MB."
        )
    if not data:
        raise ApiError(400, "EMPTY_FILE", "The file is empty.")
    return data


def clean_image(data: bytes) -> CleanImage:
    not_a_picture = ApiError(400, "INVALID_IMAGE", "Upload a JPEG or PNG picture.")
    try:
        with Image.open(io.BytesIO(data)) as picture:
            if picture.format not in FORMATS:
                raise not_a_picture
            width, height = picture.size
            if width * height > MAX_PIXELS:
                raise ApiError(400, "IMAGE_TOO_LARGE", "The picture has too many pixels.")
            kind = picture.format
            picture = ImageOps.exif_transpose(picture)  # turn upright, then forget the metadata
            if kind == "JPEG" and picture.mode not in ("RGB", "L"):
                picture = picture.convert("RGB")
            out = io.BytesIO()
            if kind == "JPEG":
                picture.save(out, "JPEG", quality=90)
            else:
                picture.save(out, "PNG", optimize=True)
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as error:
        raise not_a_picture from error
    clean = out.getvalue()
    extension, content_type = FORMATS[kind]
    return CleanImage(clean, extension, content_type, hashlib.sha256(clean).hexdigest())


def store(files_dir: Path, kind: str, image: CleanImage) -> str:
    """Save under a random name. Returns the path relative to files_dir."""
    relative = f"{FOLDERS[kind]}/{uuid.uuid4().hex}.{image.extension}"
    target = files_dir / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(image.data)
    return relative


def resolve(files_dir: Path, relative: str) -> Path:
    """The full path of a stored file. Refuses anything outside files_dir."""
    root = files_dir.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ApiError(404, "FILE_NOT_FOUND", "File not found.")
    return path


def remove(files_dir: Path, relative: str | None) -> None:
    if relative:
        resolve(files_dir, relative).unlink(missing_ok=True)


def remove_all(files_dir: Path) -> None:
    """Used by reset: delete every uploaded picture (only our own folders)."""
    for folder in FOLDERS.values():
        shutil.rmtree(files_dir / folder, ignore_errors=True)


def save_upload(db, settings, user, kind: str, stream, filename: str | None, now) -> File:
    """Check, clean and store one picture, and record it. The caller commits."""
    image = clean_image(read_limited(stream, settings.max_upload_bytes))
    relative = store(settings.files_dir, kind, image)
    record = File(
        user_id=user.id,
        kind=kind,
        original_name=(filename or "upload")[:255],
        content_type=image.content_type,
        size_bytes=len(image.data),
        storage_path=relative,
        sha256=image.sha256,
        created_at=now,
    )
    db.add(record)
    return record


def content_type_of(relative: str) -> str:
    return "image/png" if relative.endswith(".png") else "image/jpeg"
