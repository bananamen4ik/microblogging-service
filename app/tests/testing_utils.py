"""Useful frequently used functions."""

from contextlib import asynccontextmanager

from typing import (
    AsyncGenerator,
    Any
)

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
    """Session as context manager."""
    async for session in dep_get_session():
        yield session


async def get_tables_count() -> int | None:
    """Tables count."""
    session: AsyncSession

    async with get_session() as session:
        tables_count: Any = (await session.execute(
            text(
                "SELECT count(table_name) "
                "FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            )
        )).scalar()

    if tables_count is None:
        return None
    return int(tables_count)
