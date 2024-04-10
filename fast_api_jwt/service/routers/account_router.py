from typing import Dict, Any, Type

from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from fast_api_jwt.mq.app_message_queue import AppMessageQueue
from fast_api_jwt.database.mock_db import MockDB


class AccountRouter:
    def __init__(self, message_queue: Type[AppMessageQueue]):
        self.mock_db = MockDB()
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
        account = self.mock_db.get_account_by_username(username)
        logger.info(f"Retrieved account for username: {username}: {account}")
        return JSONResponse(account)

    async def get_by_account_id(self, account_id: str):
        account = self.mock_db.get_account(account_id)
        logger.info(f"Retrieved account for id: {account_id}: {account}")
        return JSONResponse(account)

    def register_account_cmd(self, account: Dict[str, Any]):
        logger.info(f"Registering account: {account}")
        metadata = self.message_queue.send_message(
            command="register_account_cmd",
            payload={'account': account}
        )
        return JSONResponse(metadata)
