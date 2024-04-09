import os

from loguru import logger
import uvicorn as uvicorn
from fastapi import Depends, FastAPI

from fast_api_jwt.commands.mqs.message_queue_facade_base import MessageQueueFacadeBase
from .dependencies import verify_jwt
from .routers.account_router import AccountRouter
from .routers.storyspace_router import StoryspaceRouter
from fast_api_jwt.commands.app_message_queue import AppMessageQueue

if os.getenv('FAST_API_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()


class FastAPIJWTService(FastAPI):
    """
    Our main FastAPI service.  When created, it adds other routers
    and dependency injection as needed.
    """

    def __init__(self):
        """ Constructor for FastAPIJWTService """
        super().__init__(
            title="Fast API JWT Example",
            description="Fast API JWT Example",
            version="1.0.0",
        )

        # Get Message Queue Facade for our environment:
        self.app_mq_facade: MessageQueueFacadeBase = AppMessageQueue().mq_facade()
        logger.info(f"Set up message queue: {self.app_mq_facade}")

    def build(self) -> FastAPI:
        """ Construct routers; injecting appropriate Message Queue Facade """
        account_router = AccountRouter(self.app_mq_facade)
        storyspace_router = StoryspaceRouter(self.app_mq_facade)

        """ Includes other routers with dependency injection """
        self.include_router(account_router.router, dependencies=[Depends(verify_jwt)])
        self.include_router(storyspace_router.router, dependencies=[Depends(verify_jwt)])

        # Add top level route; implemented by `root` method:
        self.router.add_api_route('/', self.root, methods=['GET'])
        return self

    async def root(self):
        """ Our root (/) endpoint implementation. """
        return {"msg": "Hello from our fast-api-jwt app."}


# Create instance of our class and call build:
app = FastAPIJWTService()
app.build()

# Start the service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=9000, reload=True)
