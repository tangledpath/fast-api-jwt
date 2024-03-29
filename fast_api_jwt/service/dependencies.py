import os
from typing import Annotated

from fastapi import Header, HTTPException
from loguru import logger

from fast_api_jwt.utils.jwt_util import JWTUtil

# Error messages:
ERR_AUTH_HEADER_MISSING = "authorization header missing"
ERR_INCORRECT_API_TOKEN = "Incorrect API token"


async def verify_jwt(authorization: Annotated[str | None, Header()] = None) -> None:
    """
    Verify the JWT in the authorization header.  A 401 status code is sent back if
    it is not present, malformed, or does not contain the corrrect apiKey.
    :param authorization: The authorization header
    :return:
    """
    if not authorization:
        raise HTTPException(status_code=401, detail=ERR_AUTH_HEADER_MISSING)
    try:
        jot = JWTUtil.decode_jwt(authorization)
    except BaseException as x:
        msg = f"Error decoding token {str(x)}"
        logger.error(f"[ERROR](Message: {msg})")
        raise HTTPException(status_code=401, detail=msg)

    if jot['apiKey'] != os.getenv('API_KEY'):
        raise HTTPException(status_code=401, detail=ERR_INCORRECT_API_TOKEN)
