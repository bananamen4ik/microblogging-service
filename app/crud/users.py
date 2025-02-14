"""CRUD functionality with users."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.schemas.users import (
    UserInCreate,
    UserOutCreate,
    UserSchema
)
from app.models.users import User


async def get_user_by_api_key(
        session: AsyncSession,
        api_key: str
) -> UserSchema | None:
    """Get user by api_key."""
    user: User | None = await session.scalar(
        select(User).where(
            User.api_key == api_key
        )
    )

    if user:
        return UserSchema.model_validate(user)
    return None


async def create_user(
        session: AsyncSession,
        user: UserInCreate
) -> UserOutCreate | None:
    """
    Create user.

    Args:
        session (AsyncSession): Session db.
        user (UserInCreate): User data for create.

    Returns:
        UserOutCreate | None: The data of the created user if successful,
        or None if the user creation fails.
    """
    new_user: User = User(**user.model_dump())

    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        return None

    return UserOutCreate.model_validate(new_user)
