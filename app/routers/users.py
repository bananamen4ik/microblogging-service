from typing import Annotated

from fastapi import APIRouter, Header

router = APIRouter()


@router.get("/api/users/me")
async def get_users_me(api_key: Annotated[str, Header()]):
    return api_key
