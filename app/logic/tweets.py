"""Logic functionality with tweets."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.tweets import (
    TweetSchema,
    TweetIn
)
from app.schemas.medias import MediaSchema
from app.schemas.tweets import (
    TweetOut,
    TweetAuthor,
    TweetLike
)
from app.models.tweets import Tweet
from app.models.medias import Media
from app.models.follows import Follow
from app.models.users import User
from app.crud.medias import (
    get_media_by_id,
    add_tweet_id_to_medias
)
from app.crud.tweets import (
    create_tweet as crud_create_tweet,
    get_tweet_by_id,
    delete_tweet_by_id,
    get_tweets_by_user_ids
)
from app.crud.users import get_following
from app.logic.medias import (
    delete_media_files,
    get_media_filename_by_id
)


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
        return None  # pragma: no cover

    res: bool = await add_tweet_id_to_medias(
        session,
        tweet.medias if tweet.medias else [],
        tweet_model.id
    )

    if not res:
        return None  # pragma: no cover

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


async def delete_tweet(
        session: AsyncSession,
        user_id: int,
        tweet_id: int
) -> bool:
    """Delete tweet."""
    media_id: int
    media_filenames: list[str] = []
    tweet: Tweet | None = await get_tweet_by_id(
        session,
        tweet_id
    )

    if tweet is None or tweet.user_id != user_id:
        return False

    for media_id in (tweet.medias if tweet.medias else []):
        media_filename: str | None = await get_media_filename_by_id(
            session,
            media_id
        )
        if media_filename is None:
            return False
        media_filenames.append(media_filename)

    delete_res: bool = await delete_tweet_by_id(
        session,
        tweet_id,
        commit=True
    )

    if not delete_res:
        return False  # pragma: no cover

    await delete_media_files(
        media_filenames
    )

    return True


async def get_tweets(
        session: AsyncSession,
        user_id: int
) -> list[TweetOut]:
    """Get tweets."""
    users_following: list[Follow] = await get_following(
        session,
        user_id
    )
    following_ids: list[int] = [
        following.user_id_following
        for following in users_following
    ]

    following_ids.append(user_id)

    tweets: list[Tweet] = await get_tweets_by_user_ids(
        session,
        following_ids
    )
    return await get_tweets_out(tweets)


async def get_tweets_out(
        tweets: list[Tweet]
) -> list[TweetOut]:
    """List tweets to list tweets_out."""
    tweet: Tweet
    tweets_out: list[TweetOut] = []

    for tweet in tweets:
        tweet_user: User = await tweet.awaitable_attrs.user
        tweet_attachments: list[str] = [
            f"/images/{media_filename}"
            for media_filename in await (
                tweet.awaitable_attrs.medias_filenames
            )
        ]
        tweet_likes: list[TweetLike] = [
            TweetLike(
                user_id=like_user_data.id,
                name=like_user_data.name
            )
            for like_user_data in await (
                tweet.awaitable_attrs.likes_users_data
            )
        ]

        tweets_out.append(
            TweetOut(
                id=tweet.id,
                content=tweet.main_content,
                attachments=tweet_attachments,
                author=TweetAuthor(
                    id=tweet_user.id,
                    name=tweet_user.name
                ),
                likes=tweet_likes
            )
        )

    return tweets_out
