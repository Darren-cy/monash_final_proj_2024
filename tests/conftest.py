import os
import os.path
import tempfile

import flask_migrate
import pytest
from flask.testing import FlaskClient
from sqlalchemy import URL, text

from dms import create_app, db


class AuthActions:
    _client: FlaskClient

    def __init__(self, client: FlaskClient):
        self._client = client

    def login(self, email="test@example.com", password="Test_Password_42"):
        return self._client.post(
            "/api/v1.0/session",
            json={
                "email": email,
                "password": password
            }
        )

    def logout(self):
        return self._client.delete("/api/v1.0/session")


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "r") as file:
    SQL_COMMANDS = text(file.read())


@pytest.fixture
def app():
    db_fp, db_path = tempfile.mkstemp()
    db_url = URL.create("sqlite", database=db_path)
    print(str(db_url))

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": str(db_url),
    })

    with app.app_context():
        from dms.models import (Assessment, Author, Criterion, Document,
                                Result, Submission, User,
                                submission_attachment, submission_author)
        db.create_all()
        db.session.execute(SQL_COMMANDS)
        db.session.commit()

    yield app

    os.close(db_fp)
    # os.remove(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)
