import os

import uvicorn as uvicorn
from fastapi import Depends, FastAPI

from fast_api_jwt.service import admin
from .dependencies import verify_jwt
from .routers.account_router import AccountRouter
from .routers.storyspace_router import StoryspaceRouter

# Use dotenv in development and test environments:
if os.getenv('PYTHON_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

class FastAPIJWTService(FastAPI):
    def __init__(self):
        super().__init__(
            title="Fast API JWT Example",
            description="Fast API JWT Example",
            version="1.0.0",
        )

    def create(self) -> FastAPI:
        account_router = AccountRouter()
        storyspace_router = StoryspaceRouter()

        self.include_router(account_router.router, dependencies=[Depends(verify_jwt)])
        self.include_router(storyspace_router.router, dependencies=[Depends(verify_jwt)])

        self.include_router(
            admin.router,
            prefix="/admin",
            tags=["admin"],
            dependencies=[Depends(verify_jwt)],
            responses={418: {"description": "Admin"}},
        )

        self.router.add_api_route('/', self.root, methods=['GET'])

    async def root(self):
        return {"msg": "Hello from our fast-api-jwt app."}


app = FastAPIJWTService()
app.create()

# Start the service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=9000, reload=True)
