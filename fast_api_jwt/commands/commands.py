from operator import methodcaller
from typing import Dict, Any

from loguru import logger

from fast_api_jwt.database.mock_db import MockDB


class Commands:
    @classmethod
    def process_command(cls, message: Dict[str, Any]) -> Any:
        command = message.get("command", None)
        payload = message.get("payload", None)
        if not command:
            raise ValueError("command is required to be on message.")

        if not payload:
            raise ValueError("payload is required to be on message.")

        if not hasattr(cls, command):
            raise ValueError(f"command:{command} is not present in Commands.")

        logger.info(f"Calling command: {command} with payload: {payload}")
        return getattr(cls, command)(payload)

    @classmethod
    def register_account_cmd(cls, payload: Dict[str, Any]):
        print(f"Adding account from message: {payload}")
        db = MockDB()
        account = payload.get("account", None)
        print(f"Adding account: {account}")
        db.add_account(account)
        return account
