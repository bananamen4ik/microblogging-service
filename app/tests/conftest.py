"""Global fixtures and other pytest functionality."""

from random import randint
from typing import AsyncGenerator

import pytest
import pytest_asyncio

from httpx import (
    ASGITransport,
    AsyncClient
)

from app.main import app
from app.crud.base import clear_db
from app.tests.testing_utils import (
    reset_db,
    clear_images_dir
)


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Test client FastAPI app."""
    async_client: AsyncClient

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
    await clear_images_dir()
    yield
    await clear_db()
    await clear_images_dir()


@pytest_asyncio.fixture(autouse=True)
async def reset_db_auto() -> None:
    """Auto reset DB."""
    await reset_db()


@pytest_asyncio.fixture(autouse=True)
async def clear_images_dir_auto() -> None:
    """Delete all images from images dir."""
    await clear_images_dir()


@pytest.fixture(scope="session", autouse=True)
def faker_seed() -> int:
    """Random seed for Faker package."""
    seed_min: int = 0
    seed_max: int = 10000
    return randint(seed_min, seed_max)
