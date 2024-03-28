from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/services/storyspaces",
    tags=["storyspaces"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
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

@router.get("/{storyspace_id}")
async def get_by_id(storyspace_id: str):
    logger.info(f"Getting storyspace_id: {storyspace_id}")
    storyspace = {
        'id': storyspace_id,
        'name': 'barfood'
    }
    return JSONResponse(storyspace)



@router.post("/begin")
async def begin_storyspace(username, storyspace):
    # TODO: invoke event so this command can executed asynchronously
    logger.info(f"Beginning storyspace: {storyspace} for user {username}")
    return JSONResponse({"task_id": 2113})
