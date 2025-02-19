"""CRUD functionality with tweets."""

from sqlalchemy import (
    select,
    delete
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.tweets import Tweet


async def create_tweet(
        session: AsyncSession,
        tweet: Tweet,
        commit: bool = False
) -> Tweet | None:
    """Create tweet."""
    session.add(tweet)
    try:
        if commit:
            await session.commit()  # pragma: no cover
        else:
            await session.flush()
    except SQLAlchemyError:  # pragma: no cover
        return None
    return tweet


async def get_tweet_by_id(
        session: AsyncSession,
        tweet_id: int
) -> Tweet | None:
    """Get tweet by id."""
    return await session.scalar(
        select(
            Tweet
        ).where(
            Tweet.id == tweet_id
        )
    )


async def delete_tweet_by_id(
        session: AsyncSession,
        tweet_id: int,
        commit: bool = False
) -> bool:
    """Delete tweet by id."""
    try:
        await session.execute(
            delete(Tweet).where(
                Tweet.id == tweet_id
            )
        )
    except SQLAlchemyError:  # pragma: no cover
        return False

    try:
        if commit:
            await session.commit()  # pragma: no cover
        else:
            await session.flush()
    except SQLAlchemyError:  # pragma: no cover
        return False
    return True
