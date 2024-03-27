from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/services/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{account_id}")
async def get(account_id: str):
    # TODO: get from db`

    print(f"Getting account_id: {account_id}")
    account = {
        'id': account_id,
        'username': 'foobar'
    }
    return JSONResponse(account)


@router.get('/')
async def get_account_by_username(username):
    # TODO: get from db
    account = {
        'id': 2112,
        'username': username
    }
    return JSONResponse(account)


@router.post('/register')
def register_account(account_data: dict):
    # TODO: invoke event so this command can executed asynchronously
    print(f"Registering account: {account_data}")
    return JSONResponse({"task_id": 2112})
