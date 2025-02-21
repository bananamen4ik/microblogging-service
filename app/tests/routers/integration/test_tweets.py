"""Test tweets routers module."""

from typing import Any

import pytest

import pytest_asyncio

from faker import Faker

from httpx import (
    AsyncClient,
    Response
)

from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.testing_utils import (
    LOOP_SCOPE_SESSION,
    API_KEY,
    RESULT_KEY,
    get_session
)
from app.tests.crud.test_tweets import get_tweet
from app.models.users import User
from app.models.tweets import Tweet
from app.crud.users import (
    create_user,
    get_user_by_id
)
from app.schemas.users import UserInCreate

URI_API_TWEETS: str = "/api/tweets"
URI_API_SLASH: str = "/"


class TestAPICreateTweetPostEndpoint:
    """Test create tweet API post endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self, faker: Faker) -> None:
        """Global variables for create tweet."""
        self.uri: str = URI_API_TWEETS
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
        """Global variables for delete tweet."""
        self.uri: str = URI_API_TWEETS

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
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id)
                ]),
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
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id)
                ]),
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
        """Global variables for add like tweet."""
        self.uri: str = URI_API_TWEETS
        self.uri_end: str = "likes"

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
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id),
                    self.uri_end
                ]),
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
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id),
                    self.uri_end
                ]),
                headers={
                    API_KEY: str(faker.uuid4())
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert not res_data[RESULT_KEY]
            assert res.status_code == status.HTTP_400_BAD_REQUEST


class TestAPIDeleteLikeTweetDeleteEndpoint:
    """Test delete like tweet API delete endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self) -> None:
        """Global variables for delete like tweet."""
        self.uri: str = URI_API_TWEETS
        self.uri_end: str = "likes"

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_delete_like_tweet(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test delete like tweet."""
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
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id),
                    self.uri_end
                ]),
                headers={
                    API_KEY: user.api_key
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert res_data[RESULT_KEY]

            res = await client.delete(
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id),
                    self.uri_end
                ]),
                headers={
                    API_KEY: user.api_key
                }
            )
            res_data = res.json()

            assert res_data
            assert res_data[RESULT_KEY]

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_delete_like_tweet_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test delete like tweet with user invalid."""
        session: AsyncSession

        async with get_session() as session:
            tweet: Tweet = await get_tweet(
                session,
                faker
            )
            await session.commit()

            res: Response = await client.delete(
                URI_API_SLASH.join([
                    self.uri,
                    str(tweet.id),
                    self.uri_end
                ]),
                headers={
                    API_KEY: str(faker.uuid4())
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert not res_data[RESULT_KEY]
            assert res.status_code == status.HTTP_400_BAD_REQUEST


class TestAPIGetTweetsGetEndpoint:
    """Test get tweets API get endpoint."""

    @pytest_asyncio.fixture(autouse=True)
    async def init(self) -> None:
        """Global variables for get tweets."""
        self.uri: str = URI_API_TWEETS

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_tweets(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test get tweets."""
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

            res: Response = await client.get(
                str(self.uri),
                headers={
                    API_KEY: user.api_key
                }
            )
            res_data: Any = res.json()

            assert res_data
            assert res_data[RESULT_KEY]
            assert len(res_data["tweets"])

    @pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
    async def test_get_tweets_user_invalid(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test get tweets with user invalid."""
        res: Response = await client.get(
            str(self.uri),
            headers={
                API_KEY: str(faker.uuid4())
            }
        )
        res_data: Any = res.json()

        assert res_data
        assert not res_data[RESULT_KEY]
        assert res.status_code == status.HTTP_400_BAD_REQUEST
