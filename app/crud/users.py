"""CRUD functionality with users."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.schemas.users import UserInCreate, UserOutCreate
from app.models.users import User


async def get_user(api_key: str):
    """..."""
    ...


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
