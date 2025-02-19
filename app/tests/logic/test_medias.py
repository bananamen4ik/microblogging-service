"""Test medias logic module."""

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
from app.crud.users import create_user
from app.crud.medias import create_media
from app.config import settings
from app.schemas.medias import MediaSchema
from app.models.medias import Media
from app.models.users import User
from app.logic.medias import (
    upload_image,
    save_media,
    delete_media_files,
    get_media_filename_by_id
)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_upload_image(faker: Faker) -> None:
    """Test upload image."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile()

    async with get_session() as session:
        user_model: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_model

        media: MediaSchema | None = await upload_image(
            session,
            user_model.id,
            image_file
        )
        assert media
        assert media.id == 1

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
        user_model: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_model

        assert await upload_image(
            session,
            user_model.id,
            image_file
        ) is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_upload_image_type_invalid(faker: Faker) -> None:
    """Test upload image file type invalid."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile(True)

    async with get_session() as session:
        user_moder: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_moder

        media: MediaSchema | None = await upload_image(
            session,
            user_moder.id,
            image_file
        )
        assert media is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_upload_image_invalid_user_id(faker: Faker) -> None:
    """Test upload image."""
    session: AsyncSession
    image_file: UploadFile = await get_example_image_uploadfile()

    async with get_session() as session:
        user_model: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user_model

        media: MediaSchema | None = await upload_image(
            session,
            user_model.id + 1,
            image_file
        )
        assert media is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_save_media() -> None:
    """Test save media."""
    media_file: UploadFile = await get_example_image_uploadfile()

    await save_media(
        media_file,
        settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name
    )
    assert (settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name).exists()


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_delete_media_files() -> None:
    """Test delete media files."""
    media_file: UploadFile = await get_example_image_uploadfile()

    await save_media(
        media_file,
        settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name
    )
    assert (settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name).exists()

    await delete_media_files([STATIC_IMAGE_EXAMPLE_PATH.name])
    assert not (settings.path_images / STATIC_IMAGE_EXAMPLE_PATH.name).exists()


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_media_filename_by_id(faker: Faker) -> None:
    """Test upload image."""
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

        media: Media | None = await create_media(
            session,
            Media(
                ext=faker.first_name(),
                user_id=user_model.id
            )
        )
        assert media

        media_filename: str | None = await get_media_filename_by_id(
            session,
            media.id
        )
        assert media_filename == f"{media.id}.{media.ext}"
