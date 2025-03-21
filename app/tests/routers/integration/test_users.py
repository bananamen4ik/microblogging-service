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

from app.schemas.users import (
    UserInCreate,
    UserSchema,
    UserOut,
    UserGetProfileResponse
)
from app.schemas.base import ResultResponse
from app.schemas.exceptions import MainException
from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    API_KEY
)
from app.config import settings

URI_API_USERS: str = "/api/users"
URI_API_SLASH: str = "/"


class TestAPICreateUserPostEndpoint:
    """Test create user API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for create user."""
        self.uri: str = URI_API_USERS
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_user(self, client: AsyncClient) -> None:
        """Test create user."""
        res: Response = await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )
        assert res.status_code == status.HTTP_200_OK

        res_user: UserSchema = UserSchema.model_validate(res.json())
        assert all([
            res_user.id == 1,
            res_user.name == self.name,
            res_user.api_key == self.api_key
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_user_invalid(self, client: AsyncClient) -> None:
        """Test create user with data invalid."""
        invalid_new_user: dict = {}
        res: Response = await client.post(
            self.uri,
            json=invalid_new_user
        )
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

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
        """Test create user with an existing api_key."""
        await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )

        res: Response = await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST

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
        """Test create user without debug mode."""
        settings_debug: bool = settings.debug
        settings.debug = False
        res: Response = await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res_data: Any = res.json()
        assert all([
            isinstance(res_data, dict),
            res_data["error_type"] == HTTPException.__name__,
            res.status_code == status.HTTP_403_FORBIDDEN
        ])

        settings.debug = settings_debug


class TestAPIGetMeGetEndpoint:
    """Test get user own profile API get endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for get me."""
        self.uri_create: str = URI_API_USERS
        self.uri_get: str = URI_API_SLASH.join([URI_API_USERS, "me"])
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_user(self, client: AsyncClient) -> None:
        """Test get user."""
        await client.post(
            self.uri_create,
            json=self.new_user.model_dump()
        )

        res_get: Response = await client.get(
            self.uri_get,
            headers={
                API_KEY: self.api_key
            }
        )
        res_data: UserGetProfileResponse = (
            UserGetProfileResponse.model_validate(res_get.json())
        )

        res_data_user: UserOut = UserOut.model_validate(res_data.user)
        assert all([
            res_data.result,
            res_data_user.id == 1
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_user_error(self, client: AsyncClient) -> None:
        """Test get user error with non-existent api_key."""
        res_get: Response = await client.get(
            self.uri_get,
            headers={
                API_KEY: self.api_key
            }
        )

        assert res_get.status_code == status.HTTP_400_BAD_REQUEST


class TestAPIAddFollowPostEndpoint:
    """Test add follow API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self) -> None:
        """Global variables for add follow."""
        self.uri: str = URI_API_USERS
        self.uri_end: str = "follow"

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_add_follow(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test add follow."""
        res: Response = await client.post(
            str(self.uri),
            json=UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            ).model_dump()
        )
        user_follower: UserSchema = UserSchema.model_validate(res.json())

        res = await client.post(
            str(self.uri),
            json=UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            ).model_dump()
        )
        user_following: UserSchema = UserSchema.model_validate(res.json())

        res = await client.post(
            URI_API_SLASH.join([
                self.uri,
                str(user_following.id),
                self.uri_end
            ]),
            headers={
                API_KEY: user_follower.api_key
            }
        )

        res_json: ResultResponse = ResultResponse.model_validate(res.json())
        assert res_json.result

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_add_follow_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test add follow with user invalid."""
        res: Response = await client.post(
            URI_API_SLASH.join([
                self.uri,
                str(faker.random_int()),
                self.uri_end
            ]),
            headers={
                API_KEY: str(faker.uuid4())
            }
        )
        res_json: MainException = MainException.model_validate(res.json())
        assert not res_json.result
        assert res.status_code == status.HTTP_400_BAD_REQUEST


class TestAPIDeleteFollowDeleteEndpoint:
    """Test delete follow API delete endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self) -> None:
        """Global variables for delete follow."""
        self.uri: str = URI_API_USERS
        self.uri_end: str = "follow"

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_delete_follow(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test delete follow."""
        res: Response = await client.post(
            str(self.uri),
            json=UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            ).model_dump()
        )
        user_follower: UserSchema = UserSchema.model_validate(res.json())

        res = await client.post(
            str(self.uri),
            json=UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            ).model_dump()
        )
        user_following: UserSchema = UserSchema.model_validate(res.json())

        await client.post(
            URI_API_SLASH.join([
                self.uri,
                str(user_following.id),
                self.uri_end
            ]),
            headers={
                API_KEY: user_follower.api_key
            }
        )

        res = await client.delete(
            URI_API_SLASH.join([
                self.uri,
                str(user_following.id),
                self.uri_end
            ]),
            headers={
                API_KEY: user_follower.api_key
            }
        )
        res_json: ResultResponse = ResultResponse.model_validate(res.json())
        assert res_json.result

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_delete_follow_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test delete follow with user invalid."""
        res: Response = await client.delete(
            URI_API_SLASH.join([
                self.uri,
                str(faker.random_int()),
                self.uri_end
            ]),
            headers={
                API_KEY: str(faker.uuid4())
            }
        )
        res_json: MainException = MainException.model_validate(res.json())
        assert not res_json.result
        assert res.status_code == status.HTTP_400_BAD_REQUEST


class TestAPIGetProfileByIdGetEndpoint:
    """Test get profile by id API get endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for get profile by id."""
        self.uri: str = URI_API_USERS
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_profile_by_id(self, client: AsyncClient) -> None:
        """Test get profile by id."""
        await client.post(
            self.uri,
            json=self.new_user.model_dump()
        )

        res_get: Response = await client.get(f"{self.uri}/1")
        res_data: UserGetProfileResponse = (
            UserGetProfileResponse.model_validate(res_get.json())
        )
        res_data_user: UserOut = UserOut.model_validate(res_data.user)
        assert all([
            res_data.result,
            res_data_user.id == 1
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_profile_by_id_error(self, client: AsyncClient) -> None:
        """Test get profile by id with non-existent id."""
        res_get: Response = await client.get(f"{self.uri}/1")

        assert res_get.status_code == status.HTTP_400_BAD_REQUEST
