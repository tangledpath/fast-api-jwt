import datetime
from typing import Annotated

from fastapi import Header, HTTPException
from jose import jwt

from fast_api_jwt.utils.jwt_util import JWTUtil
from fast_api_jwt.config import Config

settings = Config().settings

ERR_AUTH_HEADER_MISSING = "authorization header missing"
ERR_INCORRECT_API_TOKEN = "Incorrect API token"
async def verify_jwt(authorization: Annotated[str | None, Header()] = None):
    print("authorization: ", authorization)
    if not authorization:
        raise HTTPException(status_code=401, detail=ERR_AUTH_HEADER_MISSING)
    try:
        jot = JWTUtil.decode_jwt(authorization)
        print("JOT: ", jot)
    except BaseException as x:
        msg = f"Error decoding token {str(x)}"
        print(f"[ERROR](Message: {msg})")
        raise HTTPException(status_code=401, detail=msg)

    if jot['apiKey'] != settings['API_KEY']:
        raise HTTPException(status_code=401, detail=ERR_INCORRECT_API_TOKEN)

    # print(f"[INFO] JOT: {jot}")


def encode_jwt():
    """ Create a token to be used for authorizing API calls """
    payload = dict(
        iat=datetime.datetime.now(datetime.UTC),
        exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
        nbf=datetime.datetime.now(datetime.UTC),
        iss='fast-api-jwtp-client',
        apiKey=settings['API_KEY'],
    )

    token = jwt.encode(payload, prikey, algorithm='RS256');
    return token
    #   const jwt = await new jose.SignJWT(payload)
    # .setProtectedHeader({alg: "RS256"})
    # .setIssuedAt()
    # .setIssuer("storytangle")
    # .setAudience("storytangle-api")
    # .setExpirationTime("2h")
    # .sign(privateKey);
