from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    HTTPException,
    status
)

from app.config import settings
from app.database import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession

    async with async_session() as session:
        yield session


async def check_debug() -> bool:
    if not settings.debug:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permission"
        )
    return True
