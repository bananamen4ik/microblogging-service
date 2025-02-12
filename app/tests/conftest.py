"""Global fixtures and other pytest functionality."""

import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from app.main import app
from app.crud.base import clear_db
from app.tests.utils import reset_db


@pytest_asyncio.fixture(loop_scope="session")
async def client():
    """Test client FastAPI app."""
    async_client: AsyncClient

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def lifespan():
    """
    Initialize and shut down the test session.

    This fixture handles the setup and cleanup tasks when the
    test session starts and stops.
    """
    await reset_db()
    yield
    await clear_db()
