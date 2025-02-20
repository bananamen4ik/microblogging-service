"""API routes for interaction with users."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    status,
    Path
)
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    get_session,
    check_debug
)
from app.crud.users import (
    create_user,
    get_user_by_api_key,
    delete_follow
)
from app.schemas.users import (
    UserInCreate,
    UserSchema
)
from app.models.users import User
from app.config import (
    RESULT_KEY,
    HTTP_EXCEPTION_USER_API_KEY_INVALID
)
from app.logic.users import add_follow

router: APIRouter = APIRouter(prefix="/api/users")


@router.post("", dependencies=[Depends(check_debug)])
async def api_create_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: UserInCreate
) -> UserSchema:
    """
    Endpoint to create a new user.

    Available only with debug mode on!

    Args:
        session (AsyncSession): A database session.
        user (UserInCreate): The user data to create a new user.

    Returns:
        UserSchema: The data of the created user.

    Raises:
        HTTPException: If the user creation fails error is raised.
    """
    user_model: User | None = await create_user(
        session,
        User(**user.model_dump()),
        commit=True
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not created."
        )

    return UserSchema.model_validate(user_model)


@router.get("/me")
async def api_get_me(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()]
) -> dict:
    """Get user own profile."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    return {
        RESULT_KEY: True,
        "user": {
            "id": user_model.id,
            "name": user_model.name,
            "followers": [],
            "following": []
        }
    }


@router.post("/{user_id}/follow")
async def api_add_follow(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        user_id: Annotated[int, Path()]
) -> dict:
    """Add follow."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    res: bool = await add_follow(
        session,
        user_model.id,
        user_id
    )

    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't follow."
        )

    return {
        RESULT_KEY: True
    }


@router.delete("/{user_id}/follow")
async def api_delete_follow(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        user_id: Annotated[int, Path()]
) -> dict:
    """Delete follow."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    res_delete: bool = await delete_follow(
        session,
        user_model.id,
        user_id,
        commit=True
    )

    if not res_delete:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't delete follow."
        )

    return {
        RESULT_KEY: True
    }
