"""Test tweets crud module."""

import pytest

from faker import Faker

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    get_session,
    LOOP_SCOPE_SESSION,
    get_example_image_uploadfile
)
from app.crud.tweets import (
    create_tweet,
    get_tweet_by_id,
    delete_tweet_by_id
)
from app.crud.users import create_user
from app.crud.medias import (
    get_media_by_id,
    add_tweet_id_to_medias
)
from app.models.tweets import Tweet
from app.models.users import User
from app.models.medias import Media
from app.schemas.medias import MediaSchema
from app.logic.medias import upload_image


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


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_delete_tweet_by_id(faker: Faker) -> None:
    """Test delete tweet by id."""
    session: AsyncSession

    async with get_session() as session:
        tweet: Tweet = await get_tweet(
            session,
            faker
        )

        assert await delete_tweet_by_id(
            session,
            tweet.id
        )

        assert await get_tweet_by_id(
            session,
            tweet.id
        ) is None

        for media_id in tweet.medias if tweet.medias else []:
            media: Media | None = await get_media_by_id(
                session,
                media_id
            )
            assert media is None


async def get_tweet(
        session: AsyncSession,
        faker: Faker
) -> Tweet:
    """
    Create and return tweet.

    User and media as well created.
    """
    image_file: UploadFile = await get_example_image_uploadfile()

    user: User | None = await create_user(
        session,
        User(
            name=faker.name(),
            api_key=str(faker.uuid4())
        )
    )
    assert user

    media: MediaSchema | None = await upload_image(
        session,
        user.id,
        image_file
    )
    assert media

    tweet: Tweet | None = await create_tweet(
        session,
        Tweet(
            user_id=user.id,
            main_content=faker.text(),
            medias=[media.id]
        )
    )
    assert tweet

    assert await add_tweet_id_to_medias(
        session,
        [media.id],
        tweet.id
    )

    return tweet
