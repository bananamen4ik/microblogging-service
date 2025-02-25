"""Test tweets logic module."""

import pytest

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    get_session
)
from app.tests.crud.test_tweets import get_tweet
from app.logic.tweets import (
    create_tweet,
    get_new_medias,
    delete_tweet,
    get_tweets,
    get_tweets_out
)
from app.schemas.tweets import (
    TweetSchema,
    TweetIn,
    TweetOut
)
from app.crud.users import create_user
from app.crud.medias import create_media
from app.crud.tweets import (
    add_like_tweet,
    get_tweets_by_user_ids
)
from app.models.users import User
from app.models.medias import Media
from app.models.tweets import Tweet
from app.models.likes import Like


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_create_tweet(faker: Faker) -> None:
    """Test create tweet."""
    session: AsyncSession
    async with get_session() as session:
        user: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user

        tweet: TweetSchema | None = await create_tweet(
            session,
            TweetIn(
                user_id=user.id,
                main_content=faker.text()
            )
        )
        assert tweet


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_new_medias(faker: Faker) -> None:
    """Test get new medias."""
    session: AsyncSession
    async with get_session() as session:
        user: User | None = await create_user(
            session,
            User(
                name=faker.name(),
                api_key=str(faker.uuid4())
            )
        )
        assert user

        media: Media | None = await create_media(
            session,
            Media(
                ext=faker.first_name(),
                user_id=user.id
            )
        )
        assert media

        media_ids: list[int] | None = await get_new_medias(
            session,
            [media.id, media.id + 1],
            user.id
        )
        assert media_ids
        assert media_ids == [media.id]


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_delete_tweet(faker: Faker) -> None:
    """Test delete tweet."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        delete_res: bool = await delete_tweet(
            session,
            tweet.user_id,
            tweet.id
        )
        assert delete_res


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_delete_tweet_user_not_owner(faker: Faker) -> None:
    """Test delete tweet with user not owner."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        delete_res: bool = await delete_tweet(
            session,
            tweet.user_id + 1,
            tweet.id
        )
        assert not delete_res


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_delete_tweet_media_id_invalid(faker: Faker) -> None:
    """Test delete tweet with media id invalid."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        tweet.medias = [1, 2]

        delete_res: bool = await delete_tweet(
            session,
            tweet.user_id,
            tweet.id
        )
        assert not delete_res


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_tweets(faker: Faker) -> None:
    """Test get tweets."""
    session: AsyncSession

    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        like: Like | None = await add_like_tweet(
            session,
            Like(
                user_id=tweet.user_id,
                tweet_id=tweet.id
            )
        )
        assert like

        tweets: list[TweetOut] = await get_tweets(
            session,
            tweet.user_id
        )
        assert all([
            len(tweets),
            len(tweets[0].attachments),
            len(tweets[0].likes)
        ])


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_tweets_out(faker: Faker) -> None:
    """Test tweets to tweets out schema."""
    session: AsyncSession

    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        like: Like | None = await add_like_tweet(
            session,
            Like(
                user_id=tweet.user_id,
                tweet_id=tweet.id
            )
        )
        assert like

        tweets: list[Tweet] = await get_tweets_by_user_ids(
            session,
            [tweet.user_id]
        )
        assert len(tweets)

        tweets_out: list[TweetOut] = await get_tweets_out(tweets)
        assert all([
            len(tweets_out),
            len(tweets_out[0].attachments),
            len(tweets_out[0].likes)
        ])
