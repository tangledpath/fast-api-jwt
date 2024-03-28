from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse


class AccountRouter():
    def __init__(self):
        self.router = APIRouter(
            prefix="/service/account",
            tags=["accounts"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route('/', self.get_by_account_id, methods=['GET'])
        self.router.add_api_route('/{username}', self.get_by_username, methods=['GET'])
        self.router.add_api_route('/register', self.register_account, methods=['POST'])

    async def get_by_username(self, username: str):
        # TODO: get from db
        account = {
            'id': '2112',
            'username': username
        }
        return JSONResponse(account)

    async def get_by_account_id(self, account_id: str):
        # TODO: get from db:
        logger.info(f"Getting account_id: {account_id}")
        account = {
            'id': account_id,
            'username': 'foobar'
        }
        return JSONResponse(account)


    def register_account(self, account_data: dict):
        # TODO: invoke event so this command can executed asynchronously
        logger.info(f"Registering account: {account_data}")
        return JSONResponse({"task_id": 2112})
