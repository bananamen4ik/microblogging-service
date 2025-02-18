"""Test medias crud module."""

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from faker import Faker

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    get_session,
)
from app.models.medias import Media
from app.models.users import User
from app.models.tweets import Tweet
from app.crud.medias import (
    create_media,
    get_media_by_id,
    add_tweet_id_to_medias
)
from app.crud.users import create_user
from app.crud.tweets import create_tweet


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_create_media(faker: Faker) -> None:
    """Test create media."""
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
        assert media.tweet_id is None


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_get_media_by_id(faker: Faker) -> None:
    """Test get media by id."""
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
        assert media.tweet_id is None

        media_by_id: Media | None = await get_media_by_id(
            session,
            media.id
        )
        assert media_by_id


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_add_tweet_id_to_medias(faker: Faker) -> None:
    """Test add tweet id to medias."""
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
                main_content=faker.text()
            )
        )
        assert tweet

        media: Media | None = await create_media(
            session,
            Media(
                ext=faker.first_name(),
                user_id=user.id
            )
        )
        assert media
        assert media.tweet_id is None

        res: bool = await add_tweet_id_to_medias(
            session,
            [media.id],
            tweet.id
        )
        assert res

        media = await get_media_by_id(
            session,
            media.id
        )
        assert media
        assert media.tweet_id == tweet.id
