"""Test medias routers module."""

import pytest

from fastapi import (
    UploadFile,
    HTTPException
)

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    get_session,
    get_example_image_uploadfile
)
from app.crud.users import create_user
from app.routers.medias import api_upload_image
from app.models.users import User
from app.schemas.medias import MediaUploadImageResponse


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
        new_media: MediaUploadImageResponse = await api_upload_image(
            session,
            user_model.api_key,
            image_file
        )
        assert all([
            new_media.result,
            new_media.media_id == 1
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
