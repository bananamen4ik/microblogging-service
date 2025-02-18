"""Test tweets crud module."""

import pytest

from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION
)
from app.crud.tweets import (
    create_tweet,
    get_tweet_by_id
)
from app.crud.users import create_user
from app.models.tweets import Tweet
from app.models.users import User


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

        tweet: Tweet | None = await create_tweet(
            session,
            Tweet(
                user_id=user.id,
                main_content=faker.text(),
                medias=[1, 2]
            )
        )
        assert tweet

        tweet_by_id: Tweet | None = await get_tweet_by_id(
            session,
            tweet.id
        )
        assert tweet_by_id


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_tweet_by_id(faker: Faker) -> None:
    """Test get tweet by id."""
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

        tweet: Tweet | None = await create_tweet(
            session,
            Tweet(
                user_id=user.id,
                main_content=faker.text(),
                medias=[1, 2]
            )
        )
        assert tweet

        tweet_by_id: Tweet | None = await get_tweet_by_id(
            session,
            tweet.id
        )
        assert tweet_by_id
