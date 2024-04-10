import os
from contextlib import asynccontextmanager
from typing import Type

import uvicorn as uvicorn
from fastapi import Depends, FastAPI
from loguru import logger

from .dependencies import verify_jwt
from .routers.account_router import AccountRouter
from .routers.storyspace_router import StoryspaceRouter

from fast_api_jwt.mq.app_message_queue import AppMessageQueue

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
            on_shutdown=[self.shutdown]
        )

        # Get Message Queue Facade for our environment:
        self.message_queue: Type[AppMessageQueue] = AppMessageQueue
        logger.info(f"Set message queue: {self.message_queue}")
        self.build()
        self.startup_mq()

    def startup_mq(self):
        """ Callback for when FastAPI is started """
        logger.info(f"Starting message_queue...")
        AppMessageQueue.initialize()

    async def shutdown(self):
        """ Callback for when FastAPI is shutdown """
        logger.info(f"Shutting down message_queue...")
        self.message_queue.shutdown()

    def build(self) -> None:
        """ Construct routers; injecting appropriate Message Queue Facade """
        account_router = AccountRouter(self.message_queue)
        storyspace_router = StoryspaceRouter(self.message_queue)

        # Add top level route; implemented by `root` method:
        logger.info(f"self.router: {self.router}")
        self.add_api_route('/', self.root, methods=['GET'])

        # Include other routers with dependency injection to verify JWT:
        self.include_router(account_router.router, dependencies=[Depends(verify_jwt)]);
        self.include_router(storyspace_router.router, dependencies=[Depends(verify_jwt)])


    async def root(self):
        """ Our root (/) endpoint implementation. """
        return {"msg": "Hello from our fast-api-jwt app."}


# Create instance of our class and call build:
app = FastAPIJWTService()
# app.build()

# Start the service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=8000, reload=True)
