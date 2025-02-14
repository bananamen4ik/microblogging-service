"""Test users routers module."""

from typing import Any

import pytest
import pytest_asyncio

from httpx import (
    AsyncClient,
    Response
)

from fastapi import (
    HTTPException,
    status
)
from fastapi.exceptions import RequestValidationError

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.users import (
    api_create_user,
    api_get_me
)
from app.schemas.users import (
    UserInCreate,
    UserOutCreate
)
from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION
)
from app.config import settings


class TestAPICreateUserPostEndpoint:
    """Check create user API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for tests."""
        self.uri: str = "/api/users"
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_user(self, client: AsyncClient) -> None:
        """Check create user."""
        res: Response = await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )
        res_user: UserOutCreate = UserOutCreate.model_validate(res.json())

        assert all([
            res_user.id == 1,
            res_user.name == self.name,
            res_user.api_key == self.api_key
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_invalid_user(self, client: AsyncClient) -> None:
        """Check create user with invalid data."""
        invalid_new_user: dict = {}
        res: Response = await client.post(
            self.uri,
            json=invalid_new_user
        )
        res_data: Any = res.json()

        assert all([
            isinstance(res_data, dict),
            res_data["error_type"] == RequestValidationError.__name__,
            res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_user_exist_api_key(
            self,
            client: AsyncClient
    ) -> None:
        """Check create user with an existing api_key."""
        await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )

        res: Response = await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )
        res_data: Any = res.json()

        assert all([
            isinstance(res_data, dict),
            res_data["error_type"] == HTTPException.__name__,
            res.status_code == status.HTTP_400_BAD_REQUEST
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_user_debug_mode(
            self,
            client: AsyncClient
    ) -> None:
        """Check create user without debug mode."""
        settings_debug: bool = settings.debug
        settings.debug = False
        res: Response = await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )
        res_data: Any = res.json()

        assert all([
            isinstance(res_data, dict),
            res_data["error_type"] == HTTPException.__name__,
            res.status_code == status.HTTP_403_FORBIDDEN
        ])

        settings.debug = settings_debug


class TestAPIGetMeGetEndpoint:
    """Check get user own profile API get endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for tests."""
        self.uri_create: str = "/api/users"
        self.uri_get: str = "/api/users/me"
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_user(self, client: AsyncClient) -> None:
        """Check get user."""
        await client.post(
            self.uri_create,
            json=self.new_user.model_dump()
        )

        res_get: Response = await client.get(
            self.uri_get,
            headers={
                "api-key": self.api_key
            }
        )
        res_data: Any = res_get.json()

        assert isinstance(res_data, dict)

        res_data_user: dict = res_data["user"]
        assert all([
            res_data["result"] is True,
            res_data_user["id"] == 1
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_user_error(self, client: AsyncClient) -> None:
        """Check get user error with non-existent api_key."""
        res_get: Response = await client.get(
            self.uri_get,
            headers={
                "api-key": self.api_key
            }
        )

        assert res_get.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
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
            session,
            new_user
        )

    assert new_user_res.id == 1
    assert new_user_res.name == name
    assert new_user_res.api_key == api_key

    with pytest.raises(HTTPException):
        async with get_session() as session:
            await api_create_user(session, new_user)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_get_me(faker: Faker) -> None:
    """Check get user own profile."""
    session: AsyncSession

    new_user: UserInCreate = UserInCreate(
        name=faker.name(),
        api_key=str(faker.uuid4())
    )

    async with get_session() as session:
        new_user_res: UserOutCreate = await api_create_user(
            session,
            new_user
        )

        res_data: dict = await api_get_me(
            session,
            new_user.api_key
        )
        res_data_user: dict = res_data["user"]

        assert all([
            res_data["result"] is True,
            res_data_user["id"] == new_user_res.id
        ])

        with pytest.raises(HTTPException):
            await api_get_me(
                session,
                str(faker.uuid4())
            )
