from http import HTTPStatus

import pytest
from conftest import AuthActions
from flask.testing import FlaskClient


def test_login_valid_credentials(client: FlaskClient, auth: AuthActions):
    assert auth.login().status_code == HTTPStatus.OK


def test_login_invalid_credentials(client: FlaskClient, auth: AuthActions):
    assert auth.login(email="invalid@domain.com", password="InvalidPassword")\
        .status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.xfail
def test_logout_logged_in(app):
    raise NotImplementedError


@pytest.mark.xfail
def test_logout_not_logged_in(app):
    raise NotImplementedError
