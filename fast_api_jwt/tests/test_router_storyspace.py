import os

from fastapi.testclient import TestClient

from fast_api_jwt.database.mock_db import MockDB
from fast_api_jwt.service.dependencies import ERR_AUTH_HEADER_MISSING
from fast_api_jwt.service.main import app
from fast_api_jwt.utils.jwt_util import JWTUtil

# Client for testing app:
client = TestClient(app)
os.putenv('FAST_API_ENV', 'test')


def test_by_username_no_jwt():
    response = client.get("/service/storyspaces?username=stevenm")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_username():
    response = client.get("/service/storyspaces?username=stevenm", headers=JWTUtil.auth_header())
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 1,
            'username': 'barfood'
        },
        {
            'id': 2,
            'username': 'bazbars'
        }
    ]


def test_by_id_no_jwt():
    response = client.get("/service/storyspaces/2113")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_id():
    response = client.get("/service/storyspaces/2113", headers=JWTUtil.auth_header())
    assert response.status_code == 200
    assert response.json() == {
        'id': '2113',
        'username': 'barfood'
    }
