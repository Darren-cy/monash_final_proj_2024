from http import HTTPStatus

import pytest
from utils import dict_lists_equal

AUTHORS = (
    {"id": 1, "name": "Anh Nguyen"},
    {"id": 2, "name": "Emma Gonzalez"},
    {"id": 3, "name": "Isabella Rodriguez"},
    {"id": 4, "name": "Olivia Hansen"},
    {"id": 5, "name": "Ursula Smith"},
)


def test_get_authors(client):
    response = client.get("/api/v1.0/person")
    assert response.status_code == HTTPStatus.OK
    assert dict_lists_equal(AUTHORS, response.json)


@pytest.mark.parametrize("author", AUTHORS)
def test_get_author(client, author):
    response = client.get(f"/api/v1.0/person/{author["id"]}")
    assert response.status_code == HTTPStatus.OK
    assert response.json == author
