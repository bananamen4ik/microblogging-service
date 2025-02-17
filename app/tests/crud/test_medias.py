"""Test medias crud module."""

import pytest

from sqlalchemy import (
    select,
    and_
)
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import UploadFile

from faker import Faker

from app.tests.testing_utils import (
    STATIC_IMAGE_EXAMPLE_PATH,
    LOOP_SCOPE_SESSION,
    get_session,
    get_example_image_uploadfile
)
from app.crud.medias import (
    save_image,
    upload_image
)
from app.crud.users import create_user
from app.config import settings
from app.schemas.users import (
    UserInCreate,
    UserOutCreate
)
from app.models.medias import Media


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_upload_image(faker: Faker) -> None:
    """Test upload image."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile()

    async with get_session() as session:
        new_user: UserOutCreate | None = await create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert new_user

        media_id: int | None = await upload_image(
            session,
            new_user,
            image_file
        )
        assert media_id == 1

        new_media: Media | None = await session.scalar(
            select(Media).where(
                and_(
                    Media.id == 1,
                    Media.user_id == 1
                )
            )
        )
        assert new_media


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_upload_image_mime_type_invalid(faker: Faker) -> None:
    """Test upload image file without extension."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile(
        invalid_mime=True
    )

    async with get_session() as session:
        new_user: UserOutCreate | None = await create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert new_user

        assert await upload_image(
            session,
            new_user,
            image_file
        ) is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_upload_image_type_invalid(faker: Faker) -> None:
    """Test upload image file type invalid."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile(True)

    async with get_session() as session:
        new_user: UserOutCreate | None = await create_user(
            session,
            UserInCreate(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert new_user

        media_id: int | None = await upload_image(
            session,
            new_user,
            image_file
        )
        assert media_id is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_save_image() -> None:
    """Test save image."""
    image_file: UploadFile = await get_example_image_uploadfile()

    await save_image(
        image_file,
        settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name
    )

    assert (settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name).exists()
