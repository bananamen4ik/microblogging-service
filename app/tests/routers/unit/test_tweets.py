"""Test tweets routers module."""

import pytest

from faker import Faker

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    get_session
)
from app.tests.crud.test_tweets import get_tweet
from app.routers.tweets import (
    api_create_tweet,
    api_delete_tweet,
    api_add_like_tweet,
    api_delete_like_tweet,
    api_get_tweets
)
from app.models.users import User
from app.models.tweets import Tweet
from app.crud.users import (
    create_user,
    get_user_by_id
)
from app.schemas.tweets import (
    TweetGetTweetsResponse,
    TweetCreateTweetResponse
)
from app.schemas.base import ResultResponse


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_create_tweet(faker: Faker) -> None:
    """Test api create tweet."""
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

        res: TweetCreateTweetResponse = await api_create_tweet(
            session,
            user.api_key,
            tweet_data=faker.text()
        )
        assert all([
            res.result,
            res.tweet_id == 1
        ])


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_create_tweet_user_invalid(faker: Faker) -> None:
    """Test api create tweet with user invalid."""
    session: AsyncSession
    async with get_session() as session:
        with pytest.raises(HTTPException):
            await api_create_tweet(
                session,
                str(faker.uuid4()),
                tweet_data=faker.text()
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_delete_tweet(faker: Faker) -> None:
    """Test api delete tweet."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )
        user: User | None = await get_user_by_id(
            session,
            tweet.user_id
        )
        assert user

        res: ResultResponse = await api_delete_tweet(
            session,
            user.api_key,
            tweet.id
        )
        assert res.result


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_delete_tweet_user_invalid(faker: Faker) -> None:
    """Test api delete tweet with user invalid."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        with pytest.raises(HTTPException):
            await api_delete_tweet(
                session,
                str(faker.uuid4()),
                tweet.id
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_delete_tweet_invalid(faker: Faker) -> None:
    """Test api delete tweet with tweet invalid."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )
        user: User | None = await get_user_by_id(
            session,
            tweet.user_id
        )
        assert user

        with pytest.raises(HTTPException):
            await api_delete_tweet(
                session,
                user.api_key,
                tweet.id + 1
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_add_like_tweet(faker: Faker) -> None:
    """Test api add like to tweet."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )
        user: User | None = await get_user_by_id(
            session,
            tweet.user_id
        )
        assert user

        res: ResultResponse = await api_add_like_tweet(
            session,
            user.api_key,
            tweet.id
        )
        assert res.result


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_add_like_tweet_user_invalid(faker: Faker) -> None:
    """Test api add like to tweet with user invalid."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        with pytest.raises(HTTPException):
            await api_add_like_tweet(
                session,
                str(faker.uuid4()),
                tweet.id
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_add_like_tweet_invalid(faker: Faker) -> None:
    """Test api add like to tweet with tweet invalid."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )
        user: User | None = await get_user_by_id(
            session,
            tweet.user_id
        )
        assert user

        with pytest.raises(HTTPException):
            await api_add_like_tweet(
                session,
                user.api_key,
                tweet.id + 1
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_delete_like_tweet(faker: Faker) -> None:
    """Test api delete like in tweet."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )
        user: User | None = await get_user_by_id(
            session,
            tweet.user_id
        )
        assert user

        res: ResultResponse = await api_add_like_tweet(
            session,
            user.api_key,
            tweet.id
        )
        assert res.result

        res = await api_delete_like_tweet(
            session,
            user.api_key,
            tweet.id
        )
        assert res.result


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_delete_like_tweet_user_invalid(faker: Faker) -> None:
    """Test api delete like in tweet with user invalid."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        with pytest.raises(HTTPException):
            await api_delete_like_tweet(
                session,
                str(faker.uuid4()),
                tweet.id
            )


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_get_tweets(faker: Faker) -> None:
    """Test api get tweets."""
    session: AsyncSession
    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )
        user: User | None = await get_user_by_id(
            session,
            tweet.user_id
        )
        assert user

        res: TweetGetTweetsResponse = await api_get_tweets(
            session,
            user.api_key
        )
        assert res.result
        assert len(res.tweets)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_api_get_tweets_user_invalid(faker: Faker) -> None:
    """Test api get tweets with user invalid."""
    session: AsyncSession
    async with get_session() as session:
        with pytest.raises(HTTPException):
            await api_get_tweets(
                session,
                str(faker.uuid4())
            )
