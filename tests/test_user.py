from http import HTTPStatus

import pytest

USERS = [
    {"id":       1,
     "name":     "Test User",
     "email":    "test@example.com", },
    {"id":       2,
     "name":     "Alice Wang",
     "email":    "alice@alicesmith.net", },
    {"id":       3,
     "name":     "Bob Smith",
     "email":    "bobsmith57@gmail.com", }]


@pytest.mark.parametrize("user", USERS)
def test_get_user(client, user):
    url = f"/api/v1.0/user/{user["id"]}"
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json == user
