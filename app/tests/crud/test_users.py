"""Test users crud module."""

import pytest
from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import get_session
from app.schemas.users import (
    UserInCreate,
    UserOutCreate
)
from app.crud.users import create_user


@pytest.mark.asyncio(loop_scope="session")
async def test_create_user(faker: Faker) -> None:
    """Check create user."""
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
