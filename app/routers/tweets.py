"""API tweets for interaction with tweets."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
    Body
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from app.crud.users import get_user_by_api_key
from app.schemas.tweets import (
    TweetSchema,
    TweetIn
)
from app.models.users import User
from app.logic.tweets import create_tweet

router: APIRouter = APIRouter(prefix="/api/tweets")


@router.post("")
async def api_create_tweet(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        tweet_data: Annotated[str, Body()],
        tweet_media_ids: Annotated[list[int] | None, Body()] = None
) -> dict:
    """Create tweet."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user was not found by api_key."
        )

    tweet: TweetSchema | None = await create_tweet(
        session,
        TweetIn(
            user_id=user_model.id,
            main_content=tweet_data,
            medias=tweet_media_ids
        )
    )

    if tweet is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tweet not created."
        )

    return {
        "result": True,
        "tweet_id": tweet.id
    }
