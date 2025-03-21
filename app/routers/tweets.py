"""API tweets for interaction with tweets."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
    Body,
    Path
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from app.crud.users import get_user_by_api_key
from app.crud.tweets import (
    add_like_tweet,
    delete_like_tweet
)
from app.schemas.tweets import (
    TweetSchema,
    TweetIn,
    TweetOut,
    TweetCreateTweetResponse,
    TweetGetTweetsResponse
)
from app.schemas.base import ResultResponse
from app.models.users import User
from app.models.likes import Like
from app.logic.tweets import (
    create_tweet,
    delete_tweet,
    get_tweets
)
from app.config import HTTP_EXCEPTION_USER_API_KEY_INVALID

router: APIRouter = APIRouter(prefix="/api/tweets")


@router.post("")
async def api_create_tweet(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        tweet_data: Annotated[str, Body()],
        tweet_media_ids: Annotated[list[int] | None, Body()] = None
) -> TweetCreateTweetResponse:
    """Create tweet."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
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
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tweet not created."
        )

    return TweetCreateTweetResponse(
        result=True,
        tweet_id=tweet.id
    )


@router.delete("/{tweet_id}")
async def api_delete_tweet(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        tweet_id: Annotated[int, Path()]
) -> ResultResponse:
    """Delete tweet."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    delete_result: bool = await delete_tweet(
        session,
        user_model.id,
        tweet_id
    )

    if not delete_result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The tweet cannot be deleted."
        )

    return ResultResponse(
        result=True
    )


@router.post("/{tweet_id}/likes")
async def api_add_like_tweet(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        tweet_id: Annotated[int, Path()]
) -> ResultResponse:
    """Add like to tweet."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    like: Like | None = await add_like_tweet(
        session,
        Like(
            user_id=user_model.id,
            tweet_id=tweet_id
        ),
        commit=True
    )

    if like is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't like it."
        )

    return ResultResponse(
        result=True
    )


@router.delete("/{tweet_id}/likes")
async def api_delete_like_tweet(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        tweet_id: Annotated[int, Path()]
) -> ResultResponse:
    """Delete like in tweet."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    delete_res: bool = await delete_like_tweet(
        session,
        Like(
            user_id=user_model.id,
            tweet_id=tweet_id
        ),
        commit=True
    )

    if not delete_res:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't delete a like."
        )

    return ResultResponse(
        result=True
    )


@router.get("")
async def api_get_tweets(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()]
) -> TweetGetTweetsResponse:
    """Get tweets."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    tweets: list[TweetOut] = await get_tweets(
        session,
        user_model.id
    )

    return TweetGetTweetsResponse(
        result=True,
        tweets=tweets
    )
