import uvicorn as uvicorn
from fastapi import Depends, FastAPI

from .dependencies import verify_jwt
from .internal import admin
from .routers import account_service, storyspace_service


def create_app() -> FastAPI:
    current_app = FastAPI(
        dependencies=[Depends(verify_jwt)],
        title="Storytangle Services",
        description="Storytangle Services",
        version="1.0.0",
    )

    current_app.include_router(account_service.router, dependencies=[Depends(verify_jwt)])
    current_app.include_router(storyspace_service.router, dependencies=[Depends(verify_jwt)])
    # app.include_router(account_handler.router)
    # app.include_router(storyspace_handler.router)

    current_app.include_router(
        admin.router,
        prefix="/admin",
        tags=["admin"],
        dependencies=[Depends(verify_jwt)],
        responses={418: {"description": "Admin"}},
    )

    # current_app.celery_app = create_celery()
    return current_app


app = create_app()
# celery = app.celery_app
# celery.autodiscover_tasks()


@app.get("/")
async def root():
    return {"message": "Hello Fast API!"}


# Start the services service:
if __name__ == "__main__":
    uvicorn.run("fast_api_jwt.service.main:app", port=9000, reload=True)
