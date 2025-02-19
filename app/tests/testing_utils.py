"""Useful frequently used functions."""

from contextlib import asynccontextmanager

from io import BytesIO

from mimetypes import guess_type

from pathlib import Path

from typing import (
    AsyncGenerator,
    Any
)

from aiofiles import open as aiofiles_open
from aiofiles.threadpool.binary import AsyncBufferedIOBase

from starlette.datastructures import Headers

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.crud.base import (
    clear_db,
    init_db
)
from app.dependencies import get_session as dep_get_session
from app.config import settings

LOOP_SCOPE_SESSION: str = "session"
RESULT_KEY: str = "result"
API_KEY: str = "api-key"

STATIC_DIR: Path = Path(__file__).parent / "static"
STATIC_IMAGE_EXAMPLE_PATH: Path = STATIC_DIR / "image_example.jpg"
STATIC_TXT_EXAMPLE_PATH: Path = STATIC_DIR / "data_example.txt"


async def reset_db() -> None:
    """Drop all tables and init again."""
    await clear_db()
    await init_db()


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Session as context manager."""
    session: AsyncSession

    async for session in dep_get_session():
        yield session
        break


async def get_tables_count() -> int | None:
    """Tables count."""
    session: AsyncSession

    async with get_session() as session:
        tables_count: Any = (await session.execute(
            text(
                "SELECT count(table_name) "
                "FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            )
        )).scalar()

    if tables_count is None:
        return None
    return int(tables_count)


async def clear_images_dir() -> None:
    """Delete all images from images dir."""
    for image_file in settings.path_images.iterdir():
        image_file.unlink()


async def get_example_image_uploadfile(
        invalid_image: bool = False,
        invalid_mime: bool = False
) -> UploadFile:
    """Return example image file with type UploadFile."""
    buffer: AsyncBufferedIOBase
    image_type: str | None
    path_to_file: Path = STATIC_IMAGE_EXAMPLE_PATH

    if invalid_image:
        path_to_file = STATIC_TXT_EXAMPLE_PATH

    async with aiofiles_open(path_to_file, "rb") as buffer:
        data_next: bytes = await buffer.read(1024)
        content_file: bytes = b""

        while data_next:
            content_file += data_next
            data_next = await buffer.read(1024)

    image_type, _ = guess_type(path_to_file)

    assert image_type

    return UploadFile(
        file=BytesIO(content_file),
        size=path_to_file.stat().st_size,
        filename=path_to_file.name,
        headers=Headers({
            "content-type": (
                "image/invalid"
                if invalid_mime
                else image_type
            )
        })
    )
