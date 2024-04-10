from operator import methodcaller
from typing import Dict, Any

from fast_api_jwt.database.mock_db import MockDB


class Commands:
    @classmethod
    def process_command(cls, payload: Dict[str, Any]) -> Any:
        command = payload.get("command", None)
        if not command:
            raise ValueError("command is required to be on payload.")

        if command not in cls:
            raise ValueError(f"command:{command} is not present in Commands.")

        return methodcaller(cls)(command)

    @classmethod
    def register_account(cls, payload: Dict[str, Any]):
        db = MockDB()
        account = payload.get("account", None)
        db.add_account(account)
        return account
