"""CRUD functionality with tweets."""

from sqlalchemy import select
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
