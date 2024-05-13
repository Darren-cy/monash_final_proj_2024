import os
import tempfile

import flask_migrate
import pytest
from sqlalchemy import URL

from dms import create_app


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
        flask_migrate.upgrade()

    yield app

    os.close(db_fp)
    # os.remove(db_path)


@pytest.fixture
def context(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
