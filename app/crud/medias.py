"""CRUD functionality with medias."""

from mimetypes import guess_extension

from pathlib import Path

from aiofiles import open as aiofiles_open
from aiofiles.threadpool.binary import AsyncBufferedIOBase

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.medias import Media
from app.config import settings
from app.schemas.users import UserSchema


async def upload_image(
        session: AsyncSession,
        user: UserSchema,
        image_file: UploadFile
) -> int | None:
    """Upload image."""
    upload_dir: Path = settings.path_images

    if (
            image_file.content_type is None or
            not image_file.content_type.startswith("image/")
    ):
        return None

    file_ext: str | None = guess_extension(image_file.content_type)
    if file_ext is None:
        return None

    media: Media = Media(
        ext=file_ext[1:],
        user_id=user.id
    )

    session.add(media)
    try:
        await session.flush()
    except SQLAlchemyError:  # pragma: no cover
        return None

    media_filename: str = f"{media.id}{file_ext}"

    await save_image(
        image_file,
        upload_dir / media_filename
    )

    try:
        await session.commit()
    except SQLAlchemyError:  # pragma: no cover
        Path(upload_dir / media_filename).unlink()
        return None

    return media.id


async def save_image(
        image_file: UploadFile,
        path_to: str | Path
) -> None:
    """Save image file to path."""
    buffer: AsyncBufferedIOBase

    async with aiofiles_open(path_to, "wb") as buffer:
        content_file: bytes = await image_file.read(1024)
        while content_file:
            await buffer.write(content_file)
            content_file = await image_file.read(1024)
