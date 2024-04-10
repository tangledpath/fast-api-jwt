# FastAPI with JWT and API key
Build a FASTAPI service using a JWT to securely authenticate an API Key.  

<p>
  <img src="https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/fast_api_jwt_sm.png" align="left" width="512"/>
</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>

## Use Case
_This is appropriate for a service meant to be used application(s) also under your control.  If it is generally available to multiple clients, you should probably have an API Key per client.  If that is the case, this is still a good way to understand the basic principle of how to do this in FastAPI._

## Getting started
For this example we use [poetry](https://python-poetry.org/) as the dependency and package management.  If you don't like poetry, feel free to use your favorite (pyenv, conda, etc.).  To install poetry, see [here](https://python-poetry.org/docs/#installation).  

### OSX Installation 
Poetry requires [pipx](https://pipx.pypa.io/stable/installation/).  It can be installed on OSX via [homebrew](https://brew.sh/)  
```bash
brew install pipx
pipx install poetry
```

## Create your app
With poetry installed, you can create your initial FastAPI service:
```bash
poetry new fast-api-jwt
cd fast-api-jwt
``` 

### Project setup
* Edit pyproject.toml and ensure it looks like [this](https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/pyproject.toml).  
  * Dependencies are python (3.12), fastapi, httpx, python-jose, uvicorn, python-dotenv, and loguru.
  * We also need pytest and pytest-mock configured as test dependencies.

### FastAPI service
Create your main FastAPI service application.  This is implemented as a class here instead of a plain old python module.  We will be adding other routers, which are similarly implemented as classes.  There is a reason to implement the routers in classes which will become more clear in the next article in this series, where we add message queuing and make this production-ready using Docker and AWS.
```python
# fast_api_jwt/service/main.py
import os

import uvicorn as uvicorn
from fastapi import FastAPI

class FastAPIJWTService(FastAPI):
    """
    Our main FastAPI service.  When created, it adds other routers
    and dependency injection as needed.
    """
    
    def __init__(self):
        """ Constructor for FastAPIJWTService """
        super().__init__(
            title="Fast API JWT Example",
            description="Fast API JWT Example",
            version="1.0.0",
        )

    def build(self) -> FastAPI:
        """ Creates service.  Will include other routers with dependency injection """
        self.router.add_api_route('/', self.root, methods=['GET'])

    async def root(self):
        """ Our root (/) endpoint implementation. """
        return {"msg": "Hello from our fast-api-jwt app."}


app = FastAPIJWTService()
app.create()

# Start the service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=9000, reload=True)

```

This provides a single endpoint at `/`, as well as the built-in `/docs`.  You can run the service using:
```bash
uvicorn fast_api_jwt.service.main:app --port 9000 --reload
# OR:
python -m fast_api_jwt.service.main
```

If there weren't any problems, you should be able to visit the server:
* http://localhost:9000
* http://localhost:9000/docs

### Dependency Injection
FastAPI provides a [dependency](https://fastapi.tiangolo.com/tutorial/dependencies/) injection mechanism.  We will use that to verify the JWT and API Key:
```python
# fast_api_jwt/service/dependencies.py
import os
from typing import Annotated

from fastapi import Header, HTTPException
from loguru import logger

from fast_api_jwt.utils.jwt_util import JWTUtil

# Error messages:
ERR_AUTH_HEADER_MISSING = "authorization header missing"
ERR_INCORRECT_API_TOKEN = "Incorrect API token"
ERR_MISSING_API_TOKEN = "Missing API token"


async def verify_jwt(authorization: Annotated[str | None, Header()] = None) -> None:
    """
    Verify the JWT in the authorization header.  A 401 status code is sent back if
    it is not present, malformed, or does not contain the correct apiKey.
    :param authorization: The authorization header
    :return: None
    :raises HTTPException: Results in a 404 with error message if something goes wrong
    """
    if not authorization:
        raise HTTPException(status_code=401, detail=ERR_AUTH_HEADER_MISSING)
    try:
        jot = JWTUtil.decode_jwt(authorization)
    except BaseException as x:
        msg = f"Error decoding token: {repr(x)}"
        logger.error(f"[ERROR](Message: {msg})")
        raise HTTPException(status_code=401, detail=msg)

    if ('apiKey' not in jot) or not jot['apiKey']:
        raise HTTPException(status_code=401, detail=ERR_MISSING_API_TOKEN)
    elif jot['apiKey'] != os.getenv('API_KEY'):
        raise HTTPException(status_code=401, detail=ERR_INCORRECT_API_TOKEN)
```

As you can see, the `verify_jwt` function accepts the authorization header, which should contain a JWT with an `apiKey`.  We will get into how that is sent when we write tests.  Any client application(s) will do something similar.  For development, the necessary keys are used via a [dotenv](https://pypi.org/project/python-dotenv/) file.  For production, these environment variables should be set in your production environment.  For convenience, the `.env` is included in the [git repository](https://github.com/tangledpath/fast-api-jwt).  Normally, this should not be committed to source control, and a `.env.template` with all secret information removed is added instead.  

### JWT Util
You may have noticed the usage of [JWUtil](https://github.com/tangledpath/fast-api-jwt/blob/article1/fast_api_jwt/utils/jw_util.py):
```python
jot = JWTUtil.decode_jwt(authorization)
```

This is a simple utility class that decodes the JWT with a given authorization header.  It also contains code for encoding a JWT, which is used by the unit tests.  It uses [Jose](https://pypi.org/project/python-jose/) to encode and decode.  Here it is in its entirety:
```python
import datetime
import os
from typing import Dict, Any, Union

from jose import jwt


class JWTUtil:
    """ Utility class to decode and encode JWT tokens with a secret key and an api key. """
    @classmethod
    def decode_jwt(cls, authorization_header: str) -> Dict[str, Any]:
        """ Decode the JWT from the authorization header and return the decoded JWT (dict)"""
        return jwt.decode(authorization_header, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGORITHM')],
                          audience='fast-api-jwtp-client')

    @classmethod
    def encode_jwt(cls, api_key: Union[str, None]=None) -> str:
        """
        Returns a JWT token to be used for authorizing API calls
        :param api_key: If set to None, the `API_KEY` environment variable is used.
             If it is an empty string, the value will not be added to the payload.
             Otherwise, the passed in value will be used. This is mainly useful for
             testing different scenarios in order to ensure a graceful failure condition.
        """
        apiKey = api_key if api_key is not None else os.getenv('API_KEY')
        now = datetime.datetime.now(datetime.UTC)
        payload = dict(
            iat=now,
            exp=now + datetime.timedelta(minutes=5),
            nbf=now,
            iss='fast-api-jwtp-client',
        )
        if apiKey:
            payload['apiKey'] = apiKey

        token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
        return token

    @classmethod
    def auth_header(cls, api_key: Union[str, None]=None) -> str:
        """ Return authorization header with an encoded JWT """
        return {
            'Authorization': cls.encode_jwt(api_key=api_key)
        }
```


### Environment file
The [.env file](https://github.com/tangledpath/fast-api-jwt/blob/article1/.env) should be at the root of your project and contain these keys/values:
```dotenv
API_KEY=6f16c1a4-0de8-47ca-abbc-d7d02ea0d3ee
JWT_ALGORITHM="HS256"
JWT_SECRET_KEY=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2MrvTecJigWsgebOHo7X
LOGURU_LEVEL=DEBUG
```
Note that the `API_KEY` is a random `UUID`, and can be changed to anything else.  The `JWT_SECRET_KEY` and is a random string of characters.  

## Injecting the dependencies
Now, we will make use of our verification function.  We will also add some other routes to our `fast_api_jwt/service/main.py`.  
* Add [account_router.py](https://github.com/tangledpath/fast-api-jwt/blob/article1/fast_api_jwt/service/routers/account_router.py) and [storyspace_router.py](https://github.com/tangledpath/fast-api-jwt/blob/article1/fast_api_jwt/service/routers/storyspace_router.py) to `fast_api_jwt/service/routers`.  They can be found at https://github.com/tangledpath/fast-api-jwt/tree/master/fast_api_jwt/service/routers.
* Add these imports to `fast_api_jwt/service/main.py`
  ```python
  from .dependencies import verify_jwt
  from .routers.account_router import AccountRouter
  from .routers.storyspace_router import StoryspaceRouter
  ```
* Add this code to the `build` method of `FastAPIJWTService`: 
  ```python
  account_router = AccountRouter()
  storyspace_router = StoryspaceRouter()
  
  self.include_router(account_router.router, dependencies=[Depends(verify_jwt)])
  self.include_router(storyspace_router.router, dependencies=[Depends(verify_jwt)])
  ```
* Note the dependency injection syntax: `dependencies=[Depends(verify_jwt)]`.  Note, we left the root (`/`) endpoint unsecured, so we can still visit it as a sanity check.  
* `fast_api_jwt/service/main.py` should now look like the [main.py](https://github.com/tangledpath/fast-api-jwt/blob/article1/fast_api_jwt/service/main.py) in the git repository.  

## Testing
Our tests should verify that the absence of a JWT or API Key causes a 401 response on any route except `/` and `/docs`.  Conversely, they should also verify that passing the correct JWT/API Key will result in success (200 response).  We will also verify the returned content is as expected.  You can see in our routers that the content in question is hardcoded.  We will hook it up to a database later in the series.

### Testing a FastAPI service
Firstly, we are using [pytest](https://docs.pytest.org/) for testing.  To test a FastAPI service, create a test file, e.g., `fast_api_jwt/tests/test_router_account.py`

FastAPI provides a `TestClient` that accepts an app.  You can then use that `TestClient` to invoke endpoints on your service.  To set it up, add the following to your test:
```python
# fast_api_jwt/tests/test_router_account.py
from fastapi.testclient import TestClient
from fast_api_jwt.service.main import app
client = TestClient(app)
```
This allows us to invoke our service, e.g.,
```python
response = client.get("/service/account/ACCOUNT_USERNAME")
```

We also need to import our [JWT utility](https://github.com/tangledpath/fast-api-jwt/blob/article1/fast_api_jwt/utils/jwt_util.py) from above in order to encode the JWT and make it available as a request header, as well as 
the error messages that will be returned if any part of the request is incorrect.
```python
from fast_api_jwt.service.dependencies import ERR_AUTH_HEADER_MISSING, ERR_INCORRECT_API_TOKEN, ERR_MISSING_API_TOKEN
from fast_api_jwt.utils.jwt_util import JWTUtil
```

Here are a few of the tests that can be found within [test_router_account.py](https://github.com/tangledpath/fast-api-jwt/blob/article1/fast_api_jwt/tests/test_router_account.py).  The make sure that results are returned if the JWT and API Key are correct, and that we fail gracefully if something isn't correct. 

```python
# fast_api_jwt/tests/test_router_account.py
from fastapi.testclient import TestClient

from fast_api_jwt.service.dependencies import ERR_AUTH_HEADER_MISSING, ERR_INCORRECT_API_TOKEN, ERR_MISSING_API_TOKEN
from fast_api_jwt.service.main import app
from fast_api_jwt.utils.jwt_util import JWTUtil

""" Client for testing app: """
client = TestClient(app)
def test_by_username():
    """ Test with JWT """
    response = client.get("/service/account/stevenm", headers=JWTUtil.auth_header())
    assert response.status_code == 200
    assert response.json() == {
        'id': '2112',
        'username': 'stevenm'
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

```

## Summary
There we have it; a FastAPI service that uses a JWT to verify the API Key.
This project can be found in its entirety at https://github.com/tangledpath/fast-api-jwt.  In our next article we'll explore the use of a messaging system as part of a [CQRS](https://martinfowler.com/bliki/CQRS.html) System. We will also get this ready for deployment using [Docker](https://www.docker.com/) and [AWS](https://aws.amazon.com/).  
