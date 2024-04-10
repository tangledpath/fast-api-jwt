import os
from contextlib import asynccontextmanager
from typing import Type

import uvicorn as uvicorn
from fastapi import Depends, FastAPI
from loguru import logger

from fast_api_jwt.mq.app_message_queue import AppMessageQueue
from .dependencies import verify_jwt
from .routers.account_router import AccountRouter
from .routers.storyspace_router import StoryspaceRouter

environment = os.getenv('FAST_API_ENV', 'development')
if environment != 'production':
    from dotenv import load_dotenv

    load_dotenv(f".env.${environment}")


class FastAPIJWTService(FastAPI):
    """
    Our main FastAPI service.  When created, it adds other routers
    and dependency injection as needed.
    """

    @asynccontextmanager
    async def lifespan(self, _: FastAPI):
        print("Boom!")
        # Load the messaging system:
        AppMessageQueue.initialize()
        yield
        # Clean up and release the resources
        AppMessageQueue.shutdown()

    def __init__(self):
        print("Boom?", self.lifespan)
        """ Constructor for FastAPIJWTService """
        super().__init__(
            lifespan=self.lifespan,
            title="Fast API JWT Example",
            description="Fast API JWT Example",
            version="1.0.0",
        )

        # Get Message Queue Facade for our environment:
        self.message_queue: Type[AppMessageQueue] = AppMessageQueue
        logger.info(f"Set up message queue: {self.message_queue}")

    def build(self) -> FastAPI:
        """ Construct routers; injecting appropriate Message Queue Facade """
        account_router = AccountRouter(self.message_queue)
        storyspace_router = StoryspaceRouter(self.message_queue)

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
