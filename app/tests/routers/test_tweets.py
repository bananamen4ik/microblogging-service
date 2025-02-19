"""Test tweets routers module."""

from typing import Any

from pathlib import Path

import pytest

import pytest_asyncio

from faker import Faker

from httpx import (
    AsyncClient,
    Response
)

from fastapi import (
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    API_KEY,
    RESULT_KEY,
    get_session
)
from app.tests.crud.test_tweets import get_tweet
from app.routers.tweets import (
    api_create_tweet,
    api_delete_tweet,
    api_add_like_tweet
)
from app.models.users import User
from app.models.tweets import Tweet
from app.crud.users import (
    create_user,
    get_user_by_id
)
from app.schemas.users import UserInCreate


class TestAPICreateTweetPostEndpoint:
    """Test create tweet API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for tests."""
        self.uri: str = "/api/tweets"
        self.name: str = faker.name()
        self.api_key: str = str(faker.uuid4())
        self.new_user: UserInCreate = UserInCreate(
            name=self.name,
            api_key=self.api_key
        )

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_tweet(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test create tweet."""
        session: AsyncSession

        async with get_session() as session:
            assert await create_user(
                session,
                User(**self.new_user.model_dump()),
                commit=True
            )

            res: Response = await client.post(
                self.uri,
                headers={
                    API_KEY: self.api_key
                },
                json={
                    "tweet_data": faker.text()
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert all([
                res_data[RESULT_KEY],
                res_data["tweet_id"] == 1
            ])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_create_tweet_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test create tweet with user invalid."""
        res: Response = await client.post(
            self.uri,
            headers={
                API_KEY: self.api_key
            },
            json={
                "tweet_data": faker.text()
            }
        )
        res_data: Any = res.json()

        assert res_data
        assert all([
            not res_data[RESULT_KEY],
            res.status_code == status.HTTP_400_BAD_REQUEST
        ])


class TestAPIDeleteTweetDeleteEndpoint:
    """Test delete tweet API delete endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self) -> None:
        """Global variables for tests."""
        self.uri: Path = Path("/api/tweets")

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_delete_tweet(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test delete tweet."""
        session: AsyncSession

        async with get_session() as session:
            tweet: Tweet = await get_tweet(
                session,
                faker
            )
            await session.commit()

            user: User | None = await get_user_by_id(
                session,
                tweet.user_id
            )
            assert user

            res: Response = await client.delete(
                str(self.uri / str(tweet.id)),
                headers={
                    API_KEY: user.api_key
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert res_data[RESULT_KEY]

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_delete_tweet_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test delete tweet with user invalid."""
        session: AsyncSession

        async with get_session() as session:
            tweet: Tweet = await get_tweet(
                session,
                faker
            )
            await session.commit()

            res: Response = await client.delete(
                str(self.uri / str(tweet.id)),
                headers={
                    API_KEY: str(faker.uuid4())
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert not res_data[RESULT_KEY]
            assert res.status_code == status.HTTP_400_BAD_REQUEST


class TestAPIAddLikeTweetPostEndpoint:
    """Test add like tweet API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self) -> None:
        """Global variables for tests."""
        self.uri: Path = Path("/api/tweets")

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_add_like_tweet(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test add like tweet."""
        session: AsyncSession

        async with get_session() as session:
            tweet: Tweet = await get_tweet(
                session,
                faker
            )
            await session.commit()

            user: User | None = await get_user_by_id(
                session,
                tweet.user_id
            )
            assert user

            res: Response = await client.post(
                str(self.uri / str(tweet.id) / "likes"),
                headers={
                    API_KEY: user.api_key
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert res_data[RESULT_KEY]

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_add_like_tweet_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test add like tweet with user invalid."""
        session: AsyncSession

        async with get_session() as session:
            tweet: Tweet = await get_tweet(
                session,
                faker
            )
            await session.commit()

            res: Response = await client.post(
                str(self.uri / str(tweet.id) / "likes"),
                headers={
                    API_KEY: str(faker.uuid4())
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert not res_data[RESULT_KEY]
            assert res.status_code == status.HTTP_400_BAD_REQUEST


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

        res: dict = await api_create_tweet(
            session,
            user.api_key,
            tweet_data=faker.text()
        )
        assert all([
            res[RESULT_KEY],
            res["tweet_id"] == 1
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

        res: dict = await api_delete_tweet(
            session,
            user.api_key,
            tweet.id
        )
        assert res[RESULT_KEY]


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

        res: dict = await api_add_like_tweet(
            session,
            user.api_key,
            tweet.id
        )
        assert res[RESULT_KEY]


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
