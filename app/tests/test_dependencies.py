"""Test dependencies module."""

import pytest

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    get_session,
    check_debug
)
from app.config import settings


@pytest.mark.asyncio(loop_scope="session")
async def test_get_session() -> None:
    """Check returning async session."""
    async for session in get_session():
        assert isinstance(session, AsyncSession)


@pytest.mark.asyncio(loop_scope="session")
async def test_check_debug() -> None:
    """Check debug mode."""
    debug_mode_init: bool = settings.debug

    settings.debug = True
    assert await check_debug()

    settings.debug = False
    with pytest.raises(HTTPException):
        await check_debug()

    settings.debug = debug_mode_init
