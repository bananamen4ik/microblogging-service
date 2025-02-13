"""Useful frequently used functions."""

from contextlib import asynccontextmanager

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.crud.base import (
    clear_db,
    init_db
)
from app.dependencies import get_session as dep_get_session


async def reset_db() -> None:
    """Drop all tables and init again."""
    await clear_db()
    await init_db()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Getting a session as context manager."""
    async for session in dep_get_session():
        yield session


async def get_tables_count() -> int:
    """Returns tables count."""
    session: AsyncSession

    async with get_session() as session:
        return int((await session.execute(
            text(
                "SELECT count(table_name) "
                "FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            )
        )).scalar())
