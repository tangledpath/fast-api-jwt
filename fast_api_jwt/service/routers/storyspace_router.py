from typing import Type

from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from fast_api_jwt.mq.app_message_queue import AppMessageQueue


class StoryspaceRouter:
    def __init__(self, message_queue: Type[AppMessageQueue]):
        self.message_queue = message_queue
        self.router = APIRouter(
            prefix="/service/storyspaces",
            tags=["storyspaces"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route('/', self.get_by_username, methods=['GET'])
        self.router.add_api_route('/{storyspace_id}', self.get_by_id, methods=['GET'])
        self.router.add_api_route('/begin', self.begin_command, methods=['POST'])

    async def get_by_username(self, username: str):
        logger.info(f"Getting storyspace by username: {username}")
        storyspaces = [
            {
                'id': 1,
                'username': 'barfood'
            },
            {
                'id': 2,
                'username': 'bazbars'
            }
        ]

        return JSONResponse(storyspaces)

    async def get_by_id(self, storyspace_id: str):
        logger.info(f"Getting storyspace_id: {storyspace_id}")
        storyspace = {
            'id': storyspace_id,
            'username': 'barfood'
        }
        return JSONResponse(storyspace)

    async def begin_command(self, username, storyspace):
        # TODO: invoke event so this command can executed asynchronously
        logger.info(f"Beginning storyspace: {storyspace} for user {username}")
        return JSONResponse({"task_id": 2113})
