"""Test users logic module."""

import pytest

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    get_session
)
from app.crud.users import create_user
from app.models.users import User
from app.logic.users import add_follow


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_add_follow(faker: Faker) -> None:
    """Test add follow."""
    session: AsyncSession
    async with get_session() as session:
        user_follower: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_follower

        user_following: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_following

        follow: bool = await add_follow(
            session,
            user_follower.id,
            user_following.id
        )
        assert follow


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_add_follow_on_yourself(faker: Faker) -> None:
    """Test add follow on yourself."""
    session: AsyncSession
    async with get_session() as session:
        user_follower: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_follower

        follow: bool = await add_follow(
            session,
            user_follower.id,
            user_follower.id
        )
        assert not follow


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_add_follow_following_invalid(faker: Faker) -> None:
    """Test add follow with following invalid."""
    session: AsyncSession
    async with get_session() as session:
        user_follower: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_follower

        follow: bool = await add_follow(
            session,
            user_follower.id,
            user_follower.id + 1
        )
        assert not follow


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_add_follow_twice(faker: Faker) -> None:
    """Test add follow twice."""
    session: AsyncSession
    async with get_session() as session:
        user_follower: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_follower

        user_following: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_following

        follow: bool = await add_follow(
            session,
            user_follower.id,
            user_following.id
        )
        assert follow

        follow = await add_follow(
            session,
            user_follower.id,
            user_following.id
        )
        assert not follow
