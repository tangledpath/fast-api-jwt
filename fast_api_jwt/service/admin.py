from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "This isn't an admin interface, but could be..."}
