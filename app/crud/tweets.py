"""CRUD functionality with tweets."""

from sqlalchemy import (
    select,
    delete,
    and_
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.tweets import Tweet
from app.models.likes import Like


async def create_tweet(
        session: AsyncSession,
        tweet: Tweet,
        commit: bool = False
) -> Tweet | None:
    """Create tweet."""
    session.add(tweet)
    try:
        if commit:
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:
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
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:  # pragma: no cover
        return False
    return True


async def add_like_tweet(
        session: AsyncSession,
        like: Like,
        commit: bool = False
) -> Like | None:
    """Add like to tweet."""
    session.add(like)
    try:
        if commit:
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:
        return None
    return like


async def delete_like_tweet(
        session: AsyncSession,
        like: Like,
        commit: bool = False
) -> bool:
    """Delete like in tweet."""
    try:
        await session.execute(
            delete(Like).where(
                and_(
                    Like.user_id == like.user_id,
                    Like.tweet_id == like.tweet_id
                )
            )
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


async def get_tweet_like(
        session: AsyncSession,
        like: Like
) -> Like | None:
    """Get tweet like."""
    return await session.scalar(
        select(
            Like
        ).where(
            Like.user_id == like.user_id,
            Like.tweet_id == like.tweet_id
        )
    )
