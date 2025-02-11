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
from app.crud.users import create_user
from app.schemas.users import (
    UserInCreate,
    UserOutCreate
)

router = APIRouter(prefix="/api/users")


@router.post("", dependencies=[Depends(check_debug)])
async def api_create_user(
        user: UserInCreate,
        session: Annotated[AsyncSession, Depends(get_session)]
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
            detail="User not created"
        )

    return new_user


@router.get("/me")
async def api_get_me(
        api_key: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)]
) -> str:
    """..."""
    return api_key
