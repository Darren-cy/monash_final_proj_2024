import pytest


def test_login_valid_credentials(client, auth):
    assert auth.login().status_code == 200


@pytest.mark.xfail
def test_login_invalid_credentials(app):
    raise NotImplementedError


@pytest.mark.xfail
def test_logout_logged_in(app):
    raise NotImplementedError


@pytest.mark.xfail
def test_logout_not_logged_in(app):
    raise NotImplementedError
