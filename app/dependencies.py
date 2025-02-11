"""FastAPI dependencies for routers."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    HTTPException,
    status
)

from app.config import settings
from app.database import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Complete DB session return."""
    session: AsyncSession

    async with async_session() as session:
        yield session


async def check_debug() -> bool:
    """
    Check debug mode app setting.

    Returns:
        bool: If debug mode on return True.

    Raises:
        HTTPException: If debug mode mode off.
    """
    if not settings.debug:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permission"
        )
    return True
