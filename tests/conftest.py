import pytest

from dms import create_app


@pytest.fixture
def app():
    app = create_app({
        "testing": True,
    })
    return app


@pytest.fixture
def context(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
