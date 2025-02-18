"""Logic functionality with tweets."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.tweets import (
    TweetSchema,
    TweetIn
)
from app.schemas.medias import MediaSchema
from app.models.tweets import Tweet
from app.models.medias import Media
from app.crud.medias import (
    get_media_by_id,
    add_tweet_id_to_medias
)
from app.crud.tweets import create_tweet as crud_create_tweet


async def create_tweet(
        session: AsyncSession,
        tweet: TweetIn
) -> TweetSchema | None:
    """Create tweet."""
    tweet.medias = await get_new_medias(
        session,
        tweet.medias,
        tweet.user_id
    )
    tweet_model: Tweet | None = await crud_create_tweet(
        session,
        Tweet(**tweet.model_dump())
    )

    if tweet_model is None:
        return None

    res: bool = await add_tweet_id_to_medias(
        session,
        tweet.medias if tweet.medias else [],
        tweet_model.id
    )

    if not res:
        return None

    try:
        await session.commit()
    except SQLAlchemyError:  # pragma: no cover
        return None

    return TweetSchema.model_validate(tweet_model)


async def get_new_medias(
        session: AsyncSession,
        medias: list[int] | None,
        user_id: int
) -> list[int] | None:
    """Check media and return new valid."""
    media_id: int
    valid_medias: list[int] = []

    if medias is None:
        return None

    for media_id in medias:
        media_model: Media | None = await get_media_by_id(
            session,
            media_id
        )

        if media_model is None:
            continue

        media: MediaSchema = MediaSchema.model_validate(media_model)
        if (
                media.user_id == user_id and
                media.tweet_id is None
        ):
            valid_medias.append(media_id)
    return valid_medias
