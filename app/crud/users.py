"""CRUD functionality with users."""

from sqlalchemy import (
    select,
    delete
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.users import User
from app.models.follows import Follow


async def create_user(
        session: AsyncSession,
        user: User,
        commit: bool = False
) -> User | None:
    """
    Create user.

    Args:
        session (AsyncSession): Session db.
        user (User): User data for create.
        commit (bool): Commit or flush.

    Returns:
        User | None: The data of the created user if successful,
        or None if the user creation fails.
    """
    session.add(user)
    try:
        if commit:
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:
        return None
    return user


async def get_user_by_api_key(
        session: AsyncSession,
        api_key: str
) -> User | None:
    """Get user by api_key."""
    return await session.scalar(
        select(User).where(
            User.api_key == api_key
        )
    )


async def get_user_by_id(
        session: AsyncSession,
        user_id: int
) -> User | None:
    """Get user by id."""
    return await session.scalar(
        select(User).where(
            User.id == user_id
        )
    )


async def add_follow(
        session: AsyncSession,
        follow: Follow,
        commit: bool = False
) -> Follow | None:
    """Add follow."""
    session.add(follow)
    try:
        if commit:
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:
        return None
    return follow


async def get_follow(
        session: AsyncSession,
        follow: Follow
) -> Follow | None:
    """Get follow."""
    return await session.scalar(
        select(Follow).where(
            Follow.user_id_follower == follow.user_id_follower,
            Follow.user_id_following == follow.user_id_following
        )
    )


async def delete_follow(
        session: AsyncSession,
        follower_id: int,
        following_id: int,
        commit: bool = False
) -> bool:
    """Delete follow."""
    try:
        await session.execute(
            delete(Follow).where(
                Follow.user_id_follower == follower_id,
                Follow.user_id_following == following_id
            )
        )
    except SQLAlchemyError:  # pragma: no cover
        return False

    try:
        if commit:
            await session.commit()
        else:
            await session.flush()
    except SQLAlchemyError:  # pragma: no cover
        return False
    return True
