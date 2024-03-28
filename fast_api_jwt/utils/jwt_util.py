import datetime
import os

from jose import jwt

class JWTUtil:
    @classmethod
    def decode_jwt(cls, authorization_header: str):
        return jwt.decode(authorization_header, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('JWT_ALGORITHM')],
                          audience='fast-api-jwtp-client')

    @classmethod
    def encode_jwt(cls):
        """ Create a token to be used for authorizing API calls """
        payload = dict(
            iat=datetime.datetime.now(datetime.UTC),
            exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
            nbf=datetime.datetime.now(datetime.UTC),
            iss='fast-api-jwtp-client',
            apiKey=os.getenv('API_KEY'),
        )

        token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))
        return token

    @classmethod
    def auth_headers(cls):
        return {
            'Authorization': cls.encode_jwt()
        }
