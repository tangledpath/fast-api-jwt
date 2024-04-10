import os

from fastapi.testclient import TestClient

from fast_api_jwt.database.mock_db import MockDB
from fast_api_jwt.service.dependencies import ERR_AUTH_HEADER_MISSING, ERR_INCORRECT_API_TOKEN, ERR_MISSING_API_TOKEN
from fast_api_jwt.service.main import app
from fast_api_jwt.utils.jwt_util import JWTUtil

""" Client for testing app: """

client = TestClient(app)
mock_db = MockDB()
os.putenv('FAST_API_ENV', 'test')


def test_by_username_no_jwt():
    """ Test with no JWT """
    response = client.get("/service/account/stevenm")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_username():
    """ Test with JWT """
    response = client.get("/service/account/stevenm", headers=JWTUtil.auth_header())
    assert response.status_code == 200
    assert response.json() == {
        'id': '2112',
        'username': 'stevenm',
        'email': 'stevenm@nowhere.com'
    }


def test_by_username_bad_auth_header():
    """ Test using JWT with no api key """
    response = client.get("/service/account/stevenm", headers={'Authorization': 'aslddasskdj28283382jsdk8'})
    assert response.status_code == 401
    print("response.json():", response.json())
    assert response.json()['detail'].startswith("Error decoding token:")


def test_by_username_no_api_key():
    """ Test using JWT with no api key """
    response = client.get("/service/account/stevenm", headers=JWTUtil.auth_header(api_key=""))
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_MISSING_API_TOKEN}


def test_by_username_incorrect_api_key():
    """ Test using JWT with wrong api key: """
    response = client.get("/service/account/stevenm", headers=JWTUtil.auth_header(api_key="gobble"))
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_INCORRECT_API_TOKEN}


def test_by_account_id_no_jwt():
    """ Test with no JWT """
    response = client.get("/service/account/?account_id=2112")
    assert response.status_code == 401
    assert response.json() == {"detail": ERR_AUTH_HEADER_MISSING}


def test_by_account_id():
    """ Test with JWT """
    response = client.get("/service/account/?account_id=2113", headers=JWTUtil.auth_header())
    assert response.status_code == 200
    assert response.json() == {
        'id': '2113',
        'username': 'foobar',
        'email': 'foobar@nowhere.com'
    }


def test_command_account_register():
    """ Test with JWT """
    account = {
        'id': '2114',
        'username': 'lerxt',
        'last_name': 'Lifeson',
        'first_name': 'Alex',
        'avatar_url': None,
        'email': 'alex.lifeson@rush.com'
    }
    response = client.post("/service/account/register", headers=JWTUtil.auth_header(), json=account)
    assert response.status_code == 200
    print('response.json()::', response.json())

    db_account = mock_db.get_account('2114')
    assert db_account is not None
