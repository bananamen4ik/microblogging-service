"""Global fixtures and other pytest functionality."""

from typing import AsyncGenerator

import pytest_asyncio

from httpx import (
    ASGITransport,
    AsyncClient
)

from app.main import app
from app.crud.base import clear_db
from app.tests.testing_utils import reset_db


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async_client: AsyncClient

    """Test client FastAPI app."""
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def lifespan() -> AsyncGenerator[None, None]:
    """
    Initialize and shut down the test session.

    This fixture handles the setup and cleanup tasks when the
    test session starts and stops.
    """
    await reset_db()
    yield
    await clear_db()


@pytest_asyncio.fixture(autouse=True)
async def reset_db_auto() -> None:
    """Auto reset DB."""
    await reset_db()
