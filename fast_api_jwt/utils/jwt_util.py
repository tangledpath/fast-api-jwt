import datetime
import os

from jose import jwt

from fast_api_jwt.config import Config

if os.getenv('PYTHON_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()


class JWTUtil:
    KEY = os.getenv('JWT_SECRET_KEY')
    settings = Config().settings

    @classmethod
    def decode_jwt(cls, authorization_header: str):
        print("decode_jwt: ", authorization_header)
        return jwt.decode(authorization_header, cls.KEY, algorithms=[cls.settings['JWT_ALGORITHM']],
                          audience='fast-api-jwtp-client')

    @classmethod
    def encode_jwt(cls):
        """ Create a token to be used for authorizing API calls """
        payload = dict(
            iat=datetime.datetime.now(datetime.UTC),
            exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
            nbf=datetime.datetime.now(datetime.UTC),
            iss='fast-api-jwtp-client',
            apiKey=cls.settings['API_KEY'],
        )

        token = jwt.encode(payload, cls.KEY, algorithm=cls.settings['JWT_ALGORITHM'])
        return token

    @classmethod
    def auth_headers(cls):
        return {
            'Authorization': cls.encode_jwt()
        }
