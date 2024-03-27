from fastapi.testclient import TestClient

from fast_api_jwt.service.main import app
from fast_api_jwt.service.dependencies import ERR_AUTH_HEADER_MISSING
from fast_api_jwt.utils.jwt_util import JWTUtil
client = TestClient(app)


def test_by_username_no_jwt():
    response = client.get("/services/accounts?username=stevenm")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}
    # assert response.text.detail == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_username():
    response = client.get("/services/accounts?username=stevenm", headers=JWTUtil.auth_headers())
    assert response.status_code == 200
    assert response.json() == {
        'id': '2112',
        'username': 'stevenm'
    }

def test_by_id():
    response = client.get("/services/accounts/2112", headers=JWTUtil.auth_headers())
    assert response.status_code == 200
    assert response.json() == {
        'id': "2112",
        'username': 'foobar'
    }