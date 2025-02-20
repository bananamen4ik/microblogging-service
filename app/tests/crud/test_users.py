"""Test users crud module."""

import pytest

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION,
    COMMIT_PARAMETRIZE
)
from app.crud.users import (
    create_user,
    get_user_by_api_key,
    get_user_by_id,
    add_follow,
    get_follow
)
from app.models.users import User
from app.models.follows import Follow


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
@pytest.mark.parametrize(
    COMMIT_PARAMETRIZE,
    [True, False]
)
async def test_create_user(
        faker: Faker,
        commit: bool
) -> None:
    """Test create user."""
    session: AsyncSession

    async with get_session() as session:
        user: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            ),
            commit=commit
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


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
@pytest.mark.parametrize(
    COMMIT_PARAMETRIZE,
    [True, False]
)
async def test_add_follow(
        faker: Faker,
        commit: bool
) -> None:
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

        follow: Follow | None = await add_follow(
            session,
            Follow(
                user_id_follower=user_follower.id,
                user_id_following=user_following.id
            ),
            commit=commit
        )
        assert follow

        follow = await get_follow(
            session,
            Follow(
                user_id_follower=user_follower.id,
                user_id_following=user_following.id
            )
        )
        assert follow


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
@pytest.mark.parametrize(
    COMMIT_PARAMETRIZE,
    [True, False]
)
async def test_add_follow_following_invalid(
        faker: Faker,
        commit: bool
) -> None:
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

        user_following: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_following

        follow: Follow | None = await add_follow(
            session,
            Follow(
                user_id_follower=user_follower.id,
                user_id_following=user_following.id + 1
            ),
            commit=commit
        )
        assert follow is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_follow(faker: Faker) -> None:
    """Test get follow."""
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

        follow: Follow | None = await add_follow(
            session,
            Follow(
                user_id_follower=user_follower.id,
                user_id_following=user_following.id
            )
        )
        assert follow

        follow = await get_follow(
            session,
            Follow(
                user_id_follower=user_follower.id,
                user_id_following=user_following.id
            )
        )
        assert follow
