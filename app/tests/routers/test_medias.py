"""Test medias routers module."""

from typing import Any

import pytest

import pytest_asyncio

from fastapi import (
    UploadFile,
    HTTPException
)

from httpx import (
    AsyncClient,
    Response
)

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    RESULT_KEY,
    get_session,
    get_example_image_uploadfile
)
from app.schemas.users import UserInCreate
from app.crud.users import create_user
from app.routers.medias import api_upload_image
from app.models.users import User


class TestAPIUploadImagePostEndpoint:
    """Test upload image API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for tests."""
        self.uri: str = "/api/medias"
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_upload_image(self, client: AsyncClient) -> None:
        """Test upload image."""
        session: AsyncSession
        image_file: UploadFile = await get_example_image_uploadfile()

        async with get_session() as session:
            assert await create_user(
                session,
                User(**self.new_user.model_dump()),
                commit=True
            )

            res: Response = await client.post(
                self.uri,
                headers={
                    "api-key": self.api_key
                },
                files={
                    "file": (
                        image_file.filename,
                        await image_file.read(),
                        image_file.content_type
                    )
                }
            )
            res_data: Any = res.json()

            assert all([
                res_data,
                res_data[RESULT_KEY],
                res_data["media_id"] == 1
            ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_upload_image_type(self, client: AsyncClient) -> None:
        """Test upload image type."""
        session: AsyncSession
        image_file: UploadFile = await get_example_image_uploadfile(True)

        async with get_session() as session:
            assert await create_user(
                session,
                User(**self.new_user.model_dump())
            )

        res: Response = await client.post(
            self.uri,
            headers={
                "api-key": self.api_key
            },
            files={
                "file": (
                    image_file.filename,
                    await image_file.read(),
                    image_file.content_type
                )
            }
        )

        res_data: Any = res.json()
        assert all([
            res_data,
            not res_data[RESULT_KEY]
        ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_upload_image_not_user(self, client: AsyncClient) -> None:
        """Test upload image not user."""
        image_file: UploadFile = await get_example_image_uploadfile()
        res: Response = await client.post(
            self.uri,
            headers={
                "api-key": self.api_key
            },
            files={
                "file": (
                    image_file.filename,
                    await image_file.read(),
                    image_file.content_type
                )
            }
        )

        res_data: Any = res.json()
        assert all([
            res_data,
            not res_data[RESULT_KEY]
        ])


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_upload_image(faker: Faker) -> None:
    """Test upload image API."""
    session: AsyncSession
    async with get_session() as session:
        user_model: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_model

        image_file: UploadFile = await get_example_image_uploadfile()
        new_media: dict = await api_upload_image(
            session,
            user_model.api_key,
            image_file
        )
        assert all([
            new_media[RESULT_KEY],
            new_media["media_id"] == 1
        ])


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_upload_image_api_key_invalid(faker: Faker) -> None:
    """Test upload image with invalid user api_key API."""
    session: AsyncSession
    async with get_session() as session:
        image_file: UploadFile = await get_example_image_uploadfile()

        with pytest.raises(HTTPException):
            await api_upload_image(
                session,
                str(faker.uuid4()),
                image_file
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_upload_image_type_invalid(faker: Faker) -> None:
    """Test upload image with file type invalid API."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile(True)

    async with get_session() as session:
        user_model: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_model

        with pytest.raises(HTTPException):
            await api_upload_image(
                session,
                user_model.api_key,
                image_file
            )
