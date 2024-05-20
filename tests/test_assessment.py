import pytest
from http import HTTPStatus

ASSESSMENT_1 = {"id": 1,
                "name": "Fall of the Roman Empire",
                "ctime": "2024-04-05T09:30:00",
                "rubric": {"id": 1,
                           "name": "Rubric1.pdf"},
                "owner": {"id": 1,
                          "name": "Test User"},
                "minMarks": 0,
                "maxMarks": 20,
                "criteria": [{"id": 1,
                              "name": "Presentation",
                              "min": 0,
                              "max": 3},
                             {"id": 2,
                              "name": "Spelling and grammar",
                              "min": 0,
                              "max": 3},
                             {"id": 3,
                              "name": "Cogency of arguments",
                              "min": 0,
                              "max": 5, },
                             {"id": 4,
                              "name": "Use of primary sources",
                              "min": 0,
                              "max": 5, },
                             {"id": 5,
                              "name": "Bibliography",
                              "min": 0,
                              "max": 4, }],
                "submissions": []}


@pytest.mark.xfail
def test_get_assessments(client):
    raise NotImplementedError


# @pytest.mark.xfail
def test_get_assessment(client):
    response = client.get("/api/v1.0/assessment/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json == ASSESSMENT_1


@pytest.mark.xfail
def test_create_assessment(client):
    raise NotImplementedError
