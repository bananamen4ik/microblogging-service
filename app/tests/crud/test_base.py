"""Test base crud module."""

import pytest

from app.crud.base import (
    init_db,
    clear_db
)
from app.tests.testing_utils import (
    get_tables_count,
    LOOP_SCOPE_SESSION
)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_init_db() -> None:
    """Check init db."""
    tables_count: int | None

    await clear_db()
    tables_count = await get_tables_count()
    assert tables_count is not None
    assert tables_count == 0

    await init_db()
    tables_count = await get_tables_count()
    assert tables_count is not None
    assert tables_count > 0


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_clear_db() -> None:
    """Check clear db."""
    tables_count: int | None

    await init_db()
    tables_count = await get_tables_count()
    assert tables_count is not None
    assert tables_count > 0

    await clear_db()
    tables_count = await get_tables_count()
    assert tables_count is not None
    assert tables_count == 0
