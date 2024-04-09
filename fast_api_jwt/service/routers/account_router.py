from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from fast_api_jwt.commands.mqs.message_queue_facade_base import MessageQueueFacadeBase


class AccountRouter():
    def __init__(self, message_queue: MessageQueueFacadeBase):
        self.message_queue = message_queue
        self.router = APIRouter(
            prefix="/service/account",
            tags=["accounts"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route('/', self.get_by_account_id, methods=['GET'])
        self.router.add_api_route('/{username}', self.get_by_username, methods=['GET'])
        self.router.add_api_route('/register', self.register_account_cmd, methods=['POST'])

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

    def register_account_cmd(self, account: dict):
        logger.info(f"Registering account: {account}")
        metadata = self.message_queue.send_message({
            'command': "register_account_cmd",
            'account': 'account_data'
        })
        return JSONResponse(metadata)
