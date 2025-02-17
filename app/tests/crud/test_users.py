"""Test users crud module."""

import pytest
from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION
)
from app.schemas.users import (
    UserInCreate,
    UserOutCreate,
    UserSchema
)
from app.crud.users import (
    create_user,
    get_user_by_api_key
)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_create_user(faker: Faker) -> None:
    """Test create user."""
    session: AsyncSession

    name: str = faker.name()
    api_key: str = str(faker.uuid4())

    new_user: UserInCreate = UserInCreate(
        name=name,
        api_key=api_key
    )

    async with get_session() as session:
        new_user_res: UserOutCreate | None = await create_user(
            session,
            new_user
        )

    assert new_user_res is not None
    assert new_user_res.id == 1
    assert new_user_res.name == name
    assert new_user_res.api_key == api_key

    async with get_session() as session:
        new_user_res = await create_user(
            session,
            new_user
        )

    assert new_user_res is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_user_by_api_key(faker: Faker) -> None:
    """Test get user."""
    session: AsyncSession

    name: str = faker.name()
    api_key: str = str(faker.uuid4())

    new_user: UserInCreate = UserInCreate(
        name=name,
        api_key=api_key
    )

    async with get_session() as session:
        await create_user(
            session,
            new_user
        )

        user: UserSchema | None = await get_user_by_api_key(
            session,
            api_key
        )

        assert isinstance(user, UserSchema)

        user = await get_user_by_api_key(
            session,
            str(faker.uuid4())
        )

        assert user is None
