from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header
)
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_session, check_debug

from ..crud.users import create_user

from ..schemas.users import UserInCreate, UserOutCreate

router = APIRouter(prefix="/api/users")


@router.post("", dependencies=[Depends(check_debug)])
async def api_create_user(
        user: UserInCreate,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> UserOutCreate:
    new_user: UserOutCreate | None = await create_user(session, user)
    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="User not created"
        )

    return new_user


@router.get("/me")
async def api_get_me(
        api_key: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> str:
    return api_key
