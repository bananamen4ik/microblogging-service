"""Test tweets routers module."""

from typing import Any

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
    RESULT_KEY,
    get_session
)
from app.routers.tweets import api_create_tweet
from app.models.users import User
from app.crud.users import create_user
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
        """Test upload image."""
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
                    "api-key": self.api_key
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
    async def test_create_tweet_invalid_user(
            self,
            client: AsyncClient,
            faker: Faker
    ) -> None:
        """Test upload image."""
        res: Response = await client.post(
            self.uri,
            headers={
                "api-key": self.api_key
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
async def test_api_create_tweet_invalid_user(faker: Faker) -> None:
    """Test api create tweet."""
    session: AsyncSession
    async with get_session() as session:
        with pytest.raises(HTTPException):
            await api_create_tweet(
                session,
                str(faker.uuid4()),
                tweet_data=faker.text()
            )
