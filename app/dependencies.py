from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from .config import settings

from .database import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession

    async with async_session() as session:
        yield session


async def check_debug() -> bool:
    if not settings.debug:
        raise HTTPException(
            status_code=403,
            detail="No permission"
        )
    return True
