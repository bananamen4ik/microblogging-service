"""Test users crud module."""

import pytest

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION
)
from app.crud.users import (
    create_user,
    get_user_by_api_key,
    get_user_by_id
)
from app.models.users import User


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_create_user(faker: Faker) -> None:
    """Test create user."""
    session: AsyncSession

    async with get_session() as session:
        user: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user

        user_by_api_key: User | None = await get_user_by_api_key(
            session,
            user.api_key
        )
        assert user_by_api_key


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_user_by_api_key(faker: Faker) -> None:
    """Test get user by api key."""
    session: AsyncSession

    async with get_session() as session:
        user: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user

        user_by_api_key: User | None = await get_user_by_api_key(
            session,
            user.api_key
        )
        assert user_by_api_key


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_user_by_id(faker: Faker) -> None:
    """Test get user by id."""
    session: AsyncSession

    async with get_session() as session:
        user: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user

        user_by_id: User | None = await get_user_by_id(
            session,
            user.id
        )
        assert user_by_id
