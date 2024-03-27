from typing import Annotated

from fastapi import Header, HTTPException
from jose import jwt
from fast_api_jwt.config import Config

settings = Config().settings

with open("config/jwtRS256.key.pem") as f:
    key = f.read()


async def verify_jwt(authorization: Annotated[str | None, Header()] = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="authorization header missing")
    try:
        jot = jwt.decode(authorization, key, algorithms=["RS256"], audience='fast-api-jwtp-client')
    except BaseException as x:
        msg = f"Error decoding token {str(x)}"
        print(f"[ERROR](Message: {msg})")
        raise HTTPException(status_code=401, detail=msg)

    if jot['apiKey'] != settings['API_KEY']:
        raise HTTPException(status_code=401, detail="Incorrect or missing API Key")

    print(f"[INFO] JOT: {jot}")

    # if api_key != settings.STORYTANGLE_API_KEY
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")
