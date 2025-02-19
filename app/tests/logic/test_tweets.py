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
    delete_tweet
)
from app.schemas.tweets import (
    TweetSchema,
    TweetIn
)
from app.crud.users import create_user
from app.crud.medias import create_media
from app.models.users import User
from app.models.medias import Media
from app.models.tweets import Tweet


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
async def test_delete_tweet_invalid_media_id(faker: Faker) -> None:
    """Test delete tweet with invalid media id."""
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
