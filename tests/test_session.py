import pytest
from conftest import AuthActions
from flask.testing import FlaskClient
from http import HTTPStatus


def test_login_valid_credentials(client: FlaskClient, auth: AuthActions):
    assert auth.login().status_code == HTTPStatus.OK


def test_login_invalid_credentials(client: FlaskClient, auth: AuthActions):
    assert auth.login(email="invalid@domain.com", password="InvalidPassword") == HTTPStatus.FORBIDDEN


@pytest.mark.xfail
def test_logout_logged_in(app):
    raise NotImplementedError


@pytest.mark.xfail
def test_logout_not_logged_in(app):
    raise NotImplementedError
