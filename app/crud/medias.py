"""CRUD functionality with medias."""

from sqlalchemy import (
    select,
    update
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.medias import Media


async def create_media(
        session: AsyncSession,
        media: Media,
        commit: bool = False
) -> Media | None:
    """Create media."""
    session.add(media)
    try:
        if commit:
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:
        return None
    return media


async def get_media_by_id(
        session: AsyncSession,
        media_id: int
) -> Media | None:
    """Get media by id."""
    return await session.scalar(
        select(
            Media
        ).where(
            Media.id == media_id
        )
    )


async def add_tweet_id_to_medias(
        session: AsyncSession,
        medias: list[int],
        tweet_id: int,
        commit: bool = False
) -> bool:
    """Add tweet id to medias."""
    for media_id in medias:
        try:
            await session.execute(
                update(
                    Media
                ).where(
                    Media.id == media_id
                ).values({
                    Media.tweet_id: tweet_id
                })
            )
        except SQLAlchemyError:  # pragma: no cover
            return False

        try:
            if commit:
                await session.commit()
            else:
                await session.flush()
        except SQLAlchemyError:  # pragma: no cover
            return False
    return True
