"""Test main module."""

import pytest

from app.main import lifespan
from app.crud.base import clear_db
from app.tests.testing_utils import get_tables_count


@pytest.mark.asyncio(loop_scope="session")
async def test_lifespan() -> None:
    """Checking for correct initialization and completion."""
    await clear_db()

    tables_count: int | None = await get_tables_count()
    assert tables_count is not None
    assert tables_count == 0
    async with lifespan():
        tables_count = await get_tables_count()
        assert tables_count is not None
        assert tables_count > 0
