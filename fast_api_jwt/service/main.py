import os

import uvicorn as uvicorn
from fastapi import Depends, FastAPI

from fast_api_jwt.service import admin
from .dependencies import verify_jwt
from .routers import account_router, storyspace_router

if os.getenv('PYTHON_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

def create_app() -> FastAPI:
    current_app = FastAPI(
        title="Fast API JWT Example",
        description="Fast API JWT Example",
        version="1.0.0",
    )

    current_app.include_router(account_router.router, dependencies=[Depends(verify_jwt)])
    current_app.include_router(storyspace_router.router, dependencies=[Depends(verify_jwt)])

    current_app.include_router(
        admin.router,
        prefix="/admin",
        tags=["admin"],
        dependencies=[Depends(verify_jwt)],
        responses={418: {"description": "Admin"}},
    )

    return current_app


app = create_app()


@app.get("/")
async def read_main():
    return {"msg": "Hello from our fast-api app."}


@app.get("/")
async def root():
    return {"message": "Hello Fast API!"}


# Start the service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=9000, reload=True)
