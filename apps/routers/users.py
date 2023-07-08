from fastapi import APIRouter, Depends

from apps.dependencies import get_token_header

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_token_header)])


@router.get("/")
async def read_users():
    return [{"username": "Salem"}, {"username": "Melas"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fake current user"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}
