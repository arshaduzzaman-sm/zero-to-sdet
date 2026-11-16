# Template from Zero to SDET: https://arshaduzzaman-sm.github.io/zero-to-sdet/
"""The marker is misspelled on purpose: smok instead of smoke."""

import pytest


@pytest.mark.smok
def test_home_page_loads():
    assert True
