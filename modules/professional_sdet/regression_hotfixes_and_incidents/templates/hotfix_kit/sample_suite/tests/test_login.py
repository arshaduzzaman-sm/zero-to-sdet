# Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
import pytest

pytestmark = [pytest.mark.login, pytest.mark.regression]


@pytest.mark.smoke
def test_log_in():
    assert True


def test_wrong_password():
    assert True


def test_account_locks():
    assert True


def test_reset_password():
    assert True
