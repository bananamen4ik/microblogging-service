"""Test users routers module."""

import pytest

from fastapi import HTTPException

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.users import api_create_user
from app.schemas.users import (
    UserInCreate,
    UserOutCreate
)
from app.tests.testing_utils import get_session


@pytest.mark.asyncio(loop_scope="session")
async def test_api_create_user(faker: Faker) -> None:
    """Check create user API."""
    session: AsyncSession

    name: str = faker.name()
    api_key: str = str(faker.uuid4())

    new_user: UserInCreate = UserInCreate(
        name=name,
        api_key=api_key
    )

    async with get_session() as session:
        new_user_res: UserOutCreate = await api_create_user(
            new_user,
            session
        )

    assert new_user_res.id == 1
    assert new_user_res.name == name
    assert new_user_res.api_key == api_key

    with pytest.raises(HTTPException):
        async with get_session() as session:
            await api_create_user(new_user, session)
