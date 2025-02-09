from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header
)

from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_session

router = APIRouter(prefix="/api/users")


@router.get("/me")
async def get_me(
        api_key: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> str:
    return api_key
