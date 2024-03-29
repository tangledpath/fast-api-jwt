from fastapi.testclient import TestClient

from fast_api_jwt.service.main import app
from fast_api_jwt.utils.jwt_util import JWTUtil
from fast_api_jwt.service.dependencies import ERR_AUTH_HEADER_MISSING

# Client for testing app:
client = TestClient(app)


def test_by_username_no_jwt():
    # Test with no JWT
    response = client.get("/service/account/stevenm")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_username():
    # Test with JWT
    response = client.get("/service/account/stevenm", headers=JWTUtil.auth_headers())
    assert response.status_code == 200
    assert response.json() == {
        'id': '2112',
        'username': 'stevenm'
    }


def test_by_account_id_no_jwt():
    # Test with no JWT
    response = client.get("/service/account/?account_id=2112")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_account_id():
    # Test with JWT
    response = client.get("/service/account/?account_id=2113", headers=JWTUtil.auth_headers())
    assert response.status_code == 200
    assert response.json() == {
        'id': "2113",
        'username': 'foobar'
    }
