from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from fast_api_jwt.commands.mqs.message_queue_facade_base import MessageQueueFacadeBase


class StoryspaceRouter():
    def __init__(self, message_queue: MessageQueueFacadeBase):
        self.message_queue = message_queue
        self.router = APIRouter(
            prefix="/service/storyspaces",
            tags=["storyspaces"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route('/', self.get_by_username, methods=['GET'])
        self.router.add_api_route('/{storyspace_id}', self.get_by_id, methods=['GET'])
        self.router.add_api_route('/begin', self.begin, methods=['POST'])

    async def get_by_username(username: str):
        logger.info(f"Getting storyspace by username: {username}")
        storyspaces = [
            {
                'id': 1,
                'name': 'barfood'
            },
            {
                'id': 2,
                'name': 'bazbars'
            }
        ]

        return JSONResponse(storyspaces)

    async def get_by_id(self, storyspace_id: str):
        logger.info(f"Getting storyspace_id: {storyspace_id}")
        storyspace = {
            'id': storyspace_id,
            'name': 'barfood'
        }
        return JSONResponse(storyspace)

    async def begin(self, username, storyspace):
        # TODO: invoke event so this command can executed asynchronously
        logger.info(f"Beginning storyspace: {storyspace} for user {username}")
        return JSONResponse({"task_id": 2113})
