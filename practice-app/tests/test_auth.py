"""Sign up, verify, log in, lockout, password reset and tokens."""

import pytest

from .conftest import PASSWORD, code_in, error_code

NEW_USER = {
    "email": "New.Tester@Example.com",
    "username": "new_tester",
    "full_name": "New Tester",
    "password": "Secret123",
}


def sign_up(client, **changes):
    return client.post("/api/auth/signup", json={**NEW_USER, **changes})


def test_sign_up_verify_and_log_in(client, outbox):
    response = sign_up(client)
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == "new.tester@example.com"  # stored in lower case
    assert user["is_verified"] is False
    assert "password" not in response.text and "hash" not in response.text

    login = {"username": "new_tester", "password": "Secret123"}
    assert error_code(client.post("/api/auth/login", json=login)) == "EMAIL_NOT_VERIFIED"

    code = code_in(outbox.last_to("new.tester@example.com"))
    verify = client.post("/api/auth/verify", json={"email": NEW_USER["email"], "code": code})
    assert verify.status_code == 200
    assert client.post("/api/auth/login", json=login).status_code == 200


def test_the_same_code_works_only_once(client, outbox):
    sign_up(client)
    code = code_in(outbox.last_to("new.tester@example.com"))
    body = {"email": NEW_USER["email"], "code": code}
    assert client.post("/api/auth/verify", json=body).status_code == 200
    assert error_code(client.post("/api/auth/verify", json=body)) == "ALREADY_VERIFIED"


@pytest.mark.parametrize(
    ("changes", "code"),
    [
        ({"email": "arshad@example.com"}, "EMAIL_TAKEN"),
        ({"email": "ARSHAD@example.com"}, "EMAIL_TAKEN"),
        ({"username": "Arshad"}, "USERNAME_TAKEN"),
    ],
)
def test_sign_up_needs_a_new_email_and_username(client, changes, code):
    response = sign_up(client, **changes)
    assert response.status_code == 409
    assert error_code(response) == code


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("email", "not-an-email"),
        ("username", "ab"),
        ("username", "has space"),
        ("username", "a" * 21),
        ("password", "short1"),
        ("password", "lettersonly"),
        ("password", "12345678"),
        ("full_name", "   "),
    ],
)
def test_sign_up_checks_every_field(client, field, value):
    response = sign_up(client, **{field: value})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert [detail["field"] for detail in error["details"]] == [field]
    assert value not in response.text or field != "password"  # passwords are never echoed


def test_a_wrong_code_is_refused_and_five_wrong_tries_burn_it(client, outbox):
    sign_up(client)
    code = code_in(outbox.last_to("new.tester@example.com"))
    wrong = "000000" if code != "000000" else "111111"
    for _ in range(5):
        response = client.post("/api/auth/verify", json={"email": NEW_USER["email"], "code": wrong})
        assert error_code(response) == "INVALID_CODE"
    response = client.post("/api/auth/verify", json={"email": NEW_USER["email"], "code": code})
    assert error_code(response) == "INVALID_CODE"


def test_a_code_expires_after_10_minutes(client, outbox, clock):
    sign_up(client)
    code = code_in(outbox.last_to("new.tester@example.com"))
    clock.advance(10 * 60 + 1)
    response = client.post("/api/auth/verify", json={"email": NEW_USER["email"], "code": code})
    assert error_code(response) == "CODE_EXPIRED"


def test_a_new_code_replaces_the_old_one(client, outbox):
    sign_up(client)
    old = code_in(outbox.last_to("new.tester@example.com"))
    assert (
        client.post("/api/auth/resend-code", json={"email": NEW_USER["email"]}).status_code == 202
    )
    new = code_in(outbox.last_to("new.tester@example.com"))
    if old != new:
        response = client.post("/api/auth/verify", json={"email": NEW_USER["email"], "code": old})
        assert error_code(response) == "INVALID_CODE"
    response = client.post("/api/auth/verify", json={"email": NEW_USER["email"], "code": new})
    assert response.status_code == 200


@pytest.mark.parametrize("username", ["arshad", "arshad@example.com", "ARSHAD"])
def test_log_in_with_username_or_email(client, username):
    response = client.post("/api/auth/login", json={"username": username, "password": PASSWORD})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 30 * 60


def test_wrong_password_and_unknown_user_look_the_same(client):
    wrong_password = client.post("/api/auth/login", json={"username": "arshad", "password": "x"})
    unknown_user = client.post("/api/auth/login", json={"username": "nobody", "password": "x"})
    assert wrong_password.status_code == unknown_user.status_code == 401
    assert wrong_password.json()["error"]["message"] == unknown_user.json()["error"]["message"]


def test_five_wrong_passwords_lock_the_account_for_15_minutes(client, clock):
    wrong = {"username": "arshad", "password": "Wrong@1234"}
    right = {"username": "arshad", "password": PASSWORD}
    for _ in range(4):
        assert client.post("/api/auth/login", json=wrong).status_code == 401
    assert error_code(client.post("/api/auth/login", json=wrong)) == "ACCOUNT_LOCKED"
    assert client.post("/api/auth/login", json=right).status_code == 423  # even the right one

    clock.advance(14 * 60)
    assert client.post("/api/auth/login", json=right).status_code == 423
    clock.advance(61)
    assert client.post("/api/auth/login", json=right).status_code == 200


def test_a_good_login_resets_the_wrong_password_count(client):
    wrong = {"username": "arshad", "password": "Wrong@1234"}
    for _ in range(4):
        client.post("/api/auth/login", json=wrong)
    client.post("/api/auth/login", json={"username": "arshad", "password": PASSWORD})
    for _ in range(4):
        assert client.post("/api/auth/login", json=wrong).status_code == 401


def test_forgot_password_gives_the_same_answer_for_unknown_emails(client, outbox):
    known = client.post("/api/auth/forgot-password", json={"email": "arshad@example.com"})
    unknown = client.post("/api/auth/forgot-password", json={"email": "nobody@example.com"})
    assert known.status_code == unknown.status_code == 202
    assert known.json() == unknown.json()
    assert outbox.last_to("arshad@example.com") is not None
    assert outbox.last_to("nobody@example.com") is None


def test_reset_password_with_the_code(client, outbox):
    client.post("/api/auth/forgot-password", json={"email": "arshad@example.com"})
    code = code_in(outbox.last_to("arshad@example.com"))
    body = {"email": "arshad@example.com", "code": code, "new_password": "NewPass99"}
    assert client.post("/api/auth/reset-password", json=body).status_code == 200
    assert error_code(client.post("/api/auth/reset-password", json=body)) == "INVALID_CODE"

    old = client.post("/api/auth/login", json={"username": "arshad", "password": PASSWORD})
    new = client.post("/api/auth/login", json={"username": "arshad", "password": "NewPass99"})
    assert old.status_code == 401
    assert new.status_code == 200


def test_who_am_i_needs_a_valid_token(client, login, clock):
    missing = client.get("/api/auth/me")
    assert missing.status_code == 401
    assert error_code(missing) == "NOT_AUTHENTICATED"
    assert missing.headers["WWW-Authenticate"] == "Bearer"

    garbage = client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-token"})
    assert error_code(garbage) == "INVALID_TOKEN"

    headers = login("arshad")
    assert client.get("/api/auth/me", headers=headers).json()["username"] == "arshad"

    clock.advance(30 * 60 + 1)  # tokens last 30 minutes
    assert error_code(client.get("/api/auth/me", headers=headers)) == "INVALID_TOKEN"


def test_profile_can_change_name_and_address(client, login):
    headers = login("maria")
    body = {"full_name": "Maria L.", "shipping_address": "1 New Lane, Demo Town"}
    response = client.patch("/api/users/me", json=body, headers=headers)
    assert response.status_code == 200
    assert client.get("/api/users/me", headers=headers).json()["full_name"] == "Maria L."
