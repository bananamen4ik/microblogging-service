"""API routes for interaction with users."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    status
)
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    get_session,
    check_debug
)
from app.crud.users import (
    create_user,
    get_user_by_api_key
)
from app.schemas.users import (
    UserInCreate,
    UserOutCreate,
    UserSchema
)

router: APIRouter = APIRouter(prefix="/api/users")


@router.post("", dependencies=[Depends(check_debug)])
async def api_create_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        user: UserInCreate
) -> UserOutCreate:
    """
    Endpoint to create a new user.

    Available only with debug mode on!

    Args:
        user (UserInCreate): The user data to create a new user.
        session (AsyncSession): A database session.

    Returns:
        UserOutCreate: The data of the created user.

    Raises:
        HTTPException: If the user creation fails error is raised.
    """
    new_user: UserOutCreate | None = await create_user(session, user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not created."
        )

    return new_user


@router.get("/me")
async def api_get_me(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()]
) -> dict:
    """Get user own profile."""
    user: UserSchema | None = await get_user_by_api_key(
        session,
        api_key
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user was not found by api_key."
        )

    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [],
            "following": []
        }
    }
