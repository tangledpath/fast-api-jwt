import os

import uvicorn as uvicorn
from fastapi import Depends, FastAPI

from .dependencies import verify_jwt
from .routers.account_router import AccountRouter
from .routers.storyspace_router import StoryspaceRouter

if os.getenv('PYTHON_ENV') != 'production':
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

    def build(self) -> FastAPI:
        """ Creates service.  Includes other routers with dependency injection """
        account_router = AccountRouter()
        storyspace_router = StoryspaceRouter()

        self.include_router(account_router.router, dependencies=[Depends(verify_jwt)])
        self.include_router(storyspace_router.router, dependencies=[Depends(verify_jwt)])

        # Add top level route; implemented by `root` method:
        self.router.add_api_route('/', self.root, methods=['GET'])

    async def root(self):
        """ Our root (/) endpoint implementation. """
        return {"msg": "Hello from our fast-api-jwt app."}


# Create instance of our class and call build:
app = FastAPIJWTService()
app.build()

# Start the service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=8000, reload=True)
