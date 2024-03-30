import datetime
import os
from typing import Dict, Any, Union

from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError


class JWTUtil:
    """ Utility class to decode and encode JWT tokens with a secret key and an api key. """
    @classmethod
    def decode_jwt(cls, authorization_header: str) -> Dict[str, Any]:
        """
            Decode the JWT from the authorization header and return the
            decoded JWT (dict)

            :param authorization_header: The authorization header
            :return: The decoded JWT as a dictionary.

            :raises JWTError, ExpiredSignatureError, JWTClaimsError
        """
        return jwt.decode(authorization_header, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGORITHM')],
                          audience='fast-api-jwtp-client')

    @classmethod
    def encode_jwt(cls, api_key: Union[str, None] = None) -> str:
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
    def auth_header(cls, api_key: Union[str, None] = None) -> str:
        """ Return authorization header with an encoded JWT """
        return {
            'Authorization': cls.encode_jwt(api_key=api_key)
        }
