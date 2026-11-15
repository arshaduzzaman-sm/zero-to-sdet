"""Uploaded pictures, invoice PDFs, and sending email through SMTP (Mailpit)."""

import io
import json
import os
import smtplib
import urllib.request
from datetime import UTC, datetime

import pytest
from PIL import Image

from bookshelf.mailer import Outbox

from .conftest import CARD_DECLINED, checkout, error_code

PYTHON_BOOK = 6
INACTIVE = 13


def picture(kind="PNG", size=(40, 30), color=(30, 90, 200), exif=None) -> bytes:
    out = io.BytesIO()
    image = Image.new("RGB", size, color)
    if exif is not None:
        image.save(out, kind, exif=exif)
    else:
        image.save(out, kind)
    return out.getvalue()


def upload(client, url, headers, data, name="picture.png", content_type="image/png"):
    return client.post(url, headers=headers, files={"file": (name, data, content_type)})


# Profile pictures ------------------------------------------------------------


def test_upload_and_get_my_profile_picture(client, login):
    headers = login()
    response = upload(client, "/api/users/me/avatar", headers, picture())
    assert response.status_code == 200, response.text
    avatar_url = response.json()["avatar_url"]
    assert avatar_url == f"/api/users/{response.json()['id']}/avatar"

    got = client.get(avatar_url, headers=headers)
    assert got.status_code == 200
    assert got.headers["content-type"] == "image/png"
    assert got.headers["cache-control"] == "private, no-store"
    assert Image.open(io.BytesIO(got.content)).size == (40, 30)
    assert client.get("/api/users/me", headers=headers).json()["avatar_url"] == avatar_url


def test_a_new_picture_replaces_the_old_file(client, login, app):
    headers = login()
    upload(client, "/api/users/me/avatar", headers, picture())
    upload(client, "/api/users/me/avatar", headers, picture("JPEG"), "me.jpg", "image/jpeg")
    stored = list((app.state.settings.files_dir / "avatars").iterdir())
    assert len(stored) == 1
    assert stored[0].suffix == ".jpg"
    assert stored[0].name != "me.jpg"  # random name, never the uploaded one


def test_only_the_owner_or_an_admin_sees_a_profile_picture(client, login):
    owner = login()
    url = upload(client, "/api/users/me/avatar", owner, picture()).json()["avatar_url"]
    assert error_code(client.get(url, headers=login("maria"))) == "AVATAR_NOT_FOUND"
    assert client.get(url, headers=login("admin")).status_code == 200
    assert client.get(url).status_code == 401


def test_delete_my_profile_picture(client, login, app):
    headers = login()
    url = upload(client, "/api/users/me/avatar", headers, picture()).json()["avatar_url"]
    assert client.delete("/api/users/me/avatar", headers=headers).status_code == 204
    assert error_code(client.get(url, headers=headers)) == "AVATAR_NOT_FOUND"
    assert not list((app.state.settings.files_dir / "avatars").iterdir())
    again = client.delete("/api/users/me/avatar", headers=headers)
    assert error_code(again) == "AVATAR_NOT_FOUND"


@pytest.mark.parametrize(("data", "name", "error"), [
    (b"just some text", "notes.txt", "INVALID_IMAGE"),
    (b"\x89PNG\r\n\x1a\n" + b"not really a picture", "fake.png", "INVALID_IMAGE"),
    (picture("GIF"), "moving.gif", "INVALID_IMAGE"),
    (b"", "empty.png", "EMPTY_FILE"),
])  # fmt: skip
def test_files_that_are_not_jpeg_or_png_are_refused(client, login, data, name, error):
    response = upload(client, "/api/users/me/avatar", login(), data, name)
    assert response.status_code == 400
    assert error_code(response) == error


def test_a_file_over_the_limit_is_refused(client, login, app):
    app.state.settings.max_upload_bytes = 1000
    big = picture(size=(300, 300), color=(1, 2, 3)) + b"\0" * 2000
    response = upload(client, "/api/users/me/avatar", login(), big)
    assert response.status_code == 413
    assert error_code(response) == "FILE_TOO_LARGE"


def test_hidden_metadata_is_removed(client, login):
    exif = Image.Exif()
    exif[0x010F] = "Example Camera Maker"  # the kind of detail a phone adds
    headers = login()
    data = picture("JPEG", exif=exif.tobytes())
    assert b"Example Camera Maker" in data
    url = upload(client, "/api/users/me/avatar", headers, data, "photo.jpg", "image/jpeg")
    saved = client.get(url.json()["avatar_url"], headers=headers).content
    assert b"Example Camera Maker" not in saved


def test_the_file_needs_a_login(client):
    response = upload(client, "/api/users/me/avatar", {}, picture())
    assert response.status_code == 401


# Product images --------------------------------------------------------------


def test_admin_uploads_a_product_image_that_everyone_can_see(client, login):
    response = upload(client, f"/api/products/{PYTHON_BOOK}/image", login("admin"), picture())
    assert response.status_code == 200, response.text
    image_url = response.json()["image_url"]
    assert image_url == f"/api/products/{PYTHON_BOOK}/image"
    assert client.get(image_url).headers["content-type"] == "image/png"
    assert client.get(f"/api/products/{PYTHON_BOOK}").json()["image_url"] == image_url


def test_customers_cannot_upload_product_images(client, login):
    response = upload(client, f"/api/products/{PYTHON_BOOK}/image", login(), picture())
    assert error_code(response) == "FORBIDDEN"


def test_product_without_an_image(client):
    assert client.get(f"/api/products/{PYTHON_BOOK}").json()["image_url"] is None
    assert error_code(client.get(f"/api/products/{PYTHON_BOOK}/image")) == "FILE_NOT_FOUND"
    assert error_code(client.get(f"/api/products/{INACTIVE}/image")) == "PRODUCT_NOT_FOUND"


def test_reset_removes_uploaded_pictures(client, login, app):
    admin = login("admin")
    upload(client, f"/api/products/{PYTHON_BOOK}/image", admin, picture())
    assert client.post("/api/admin/reset", headers=admin).status_code == 200
    assert not (app.state.settings.files_dir / "product-images").exists()
    assert client.get(f"/api/products/{PYTHON_BOOK}").json()["image_url"] is None


# Invoices --------------------------------------------------------------------


def test_download_the_invoice_of_a_paid_order(client, login):
    response = client.get("/api/orders/1/invoice.pdf", headers=login())
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["content-disposition"] == (
        'attachment; filename="bookshelf-invoice-1.pdf"'
    )
    assert response.content.startswith(b"%PDF-")


def test_no_invoice_for_someone_elses_order(client, login):
    maria_order = 2
    response = client.get(f"/api/orders/{maria_order}/invoice.pdf", headers=login())
    assert error_code(response) == "ORDER_NOT_FOUND"


def test_no_invoice_for_an_unpaid_order(client, login):
    headers = login()
    client.post("/api/cart/items", json={"product_id": PYTHON_BOOK, "quantity": 1}, headers=headers)
    order_id = checkout(client, headers, CARD_DECLINED).json()["error"]["details"]["order_id"]
    response = client.get(f"/api/orders/{order_id}/invoice.pdf", headers=headers)
    assert response.status_code == 409
    assert error_code(response) == "INVOICE_NOT_AVAILABLE"


# Email through SMTP ----------------------------------------------------------

NOW = datetime(2026, 5, 1, 10, 0, tzinfo=UTC)


class FakeSmtp:
    """Stands in for smtplib.SMTP and keeps what would have been sent."""

    sent: list = []
    fail = False

    def __init__(self, host, port, timeout):
        if FakeSmtp.fail:
            raise ConnectionRefusedError("nothing is listening")
        self.address = (host, port)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def send_message(self, message):
        FakeSmtp.sent.append((self.address, message))

    def noop(self):
        return (250, b"OK")


@pytest.fixture
def fake_smtp(monkeypatch):
    FakeSmtp.sent = []
    FakeSmtp.fail = False
    monkeypatch.setattr(smtplib, "SMTP", FakeSmtp)
    return FakeSmtp


def test_with_smtp_host_emails_go_to_the_smtp_server(fake_smtp):
    outbox = Outbox(smtp_host="127.0.0.1", smtp_port=51025)
    outbox.send("arshad@example.com", "Your code", "Your code is 123456.", NOW)
    ((address, message),) = fake_smtp.sent
    assert address == ("127.0.0.1", 51025)
    assert message["To"] == "arshad@example.com"
    assert message["From"] == "Bookshelf <no-reply@bookshelf.example>"
    assert message["Subject"] == "Your code"
    assert "123456" in message.get_content()
    assert outbox.last_to("arshad@example.com").subject == "Your code"
    assert outbox.is_up() == "up"


def test_a_failed_send_does_not_crash(fake_smtp, caplog):
    fake_smtp.fail = True
    outbox = Outbox(smtp_host="127.0.0.1", smtp_port=51025)
    outbox.send("arshad@example.com", "Your code", "Your code is 123456.", NOW)
    assert "Is Mailpit running?" in caplog.text
    assert outbox.last_to("arshad@example.com") is not None  # tests can still read it
    assert outbox.is_up() == "down"


def test_without_smtp_emails_are_saved_as_text_files(tmp_path):
    outbox = Outbox(tmp_path)
    outbox.send("arshad@example.com", "Your code", "Your code is 123456.", NOW)
    (saved,) = tmp_path.iterdir()
    assert "Your code is 123456." in saved.read_text()
    assert outbox.is_up() == "console"


# Real Mailpit (docker compose up -d), e.g. BOOKSHELF_TEST_MAILPIT=127.0.0.1:51025:58025
MAILPIT = os.environ.get("BOOKSHELF_TEST_MAILPIT", "")


@pytest.mark.skipif(not MAILPIT, reason="set BOOKSHELF_TEST_MAILPIT to test real Mailpit")
def test_mailpit_receives_the_email():
    host, smtp_port, web_port = MAILPIT.split(":")
    outbox = Outbox(smtp_host=host, smtp_port=int(smtp_port))
    to = f"mailpit-check-{os.getpid()}@example.com"
    outbox.send(to, "Mailpit check", "Your code is 654321.", NOW)
    url = f"http://{host}:{web_port}/api/v1/search?query=to:{to}"
    with urllib.request.urlopen(url, timeout=5) as reply:  # noqa: S310 (local test URL)
        found = json.load(reply)
    assert found["messages_count"] == 1
    assert found["messages"][0]["Subject"] == "Mailpit check"
