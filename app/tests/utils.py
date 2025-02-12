"""Useful frequently used functions."""

from app.crud.base import clear_db, init_db


async def reset_db() -> None:
    """Drop all tables and init again."""
    await clear_db()
    await init_db()
