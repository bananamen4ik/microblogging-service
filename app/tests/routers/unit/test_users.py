"""Test users routers module."""

import pytest

from fastapi import HTTPException

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.users import (
    api_create_user,
    api_get_me,
    api_add_follow
)
from app.schemas.users import (
    UserInCreate,
    UserSchema
)
from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION,
    RESULT_KEY
)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_create_user(faker: Faker) -> None:
    """Test create user API."""
    session: AsyncSession

    name: str = faker.name()
    api_key: str = str(faker.uuid4())

    new_user: UserInCreate = UserInCreate(
        name=name,
        api_key=api_key
    )

    async with get_session() as session:
        new_user_res: UserSchema = await api_create_user(
            session,
            new_user
        )

    assert all([
        new_user_res.id == 1,
        new_user_res.name == name,
        new_user_res.api_key == api_key
    ])

    with pytest.raises(HTTPException):
        async with get_session() as session:
            await api_create_user(session, new_user)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_get_me(faker: Faker) -> None:
    """Test get user own profile."""
    session: AsyncSession

    new_user: UserInCreate = UserInCreate(
        name=faker.name(),
        api_key=str(faker.uuid4())
    )

    async with get_session() as session:
        new_user_res: UserSchema = await api_create_user(
            session,
            new_user
        )

        res_data: dict = await api_get_me(
            session,
            new_user.api_key
        )
        res_data_user: dict = res_data["user"]

        assert all([
            res_data[RESULT_KEY] is True,
            res_data_user["id"] == new_user_res.id
        ])

        with pytest.raises(HTTPException):
            await api_get_me(
                session,
                str(faker.uuid4())
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_add_follow(faker: Faker) -> None:
    """Test add follow API."""
    session: AsyncSession

    async with get_session() as session:
        user_follower: UserSchema = await api_create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        user_following: UserSchema = await api_create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )

        follow: dict = await api_add_follow(
            session,
            user_follower.api_key,
            user_following.id
        )
        assert follow[RESULT_KEY]


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_add_follow_user_invalid(faker: Faker) -> None:
    """Test add follow API with user invalid."""
    session: AsyncSession

    async with get_session() as session:
        with pytest.raises(HTTPException):
            await api_add_follow(
                session,
                str(faker.uuid4()),
                faker.random_int()
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_add_follow_following_invalid(faker: Faker) -> None:
    """Test add follow API with following invalid."""
    session: AsyncSession

    async with get_session() as session:
        user_follower: UserSchema = await api_create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        user_following: UserSchema = await api_create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )

        with pytest.raises(HTTPException):
            await api_add_follow(
                session,
                user_follower.api_key,
                user_following.id + 1
            )
