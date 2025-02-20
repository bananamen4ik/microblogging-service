"""Logic functionality with users."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import (
    get_user_by_id,
    add_follow as crud_add_follow
)
from app.models.users import User
from app.models.follows import Follow


async def add_follow(
        session: AsyncSession,
        user_id_follower: int,
        user_id_following: int
) -> bool:
    """Add follow."""
    user_following: User | None = await get_user_by_id(
        session,
        user_id_following
    )

    if (
            user_id_follower == user_id_following or
            user_following is None
    ):
        return False

    res: Follow | None = await crud_add_follow(
        session,
        Follow(
            user_id_follower=user_id_follower,
            user_id_following=user_id_following
        ),
        commit=True
    )

    if res is None:
        return False
    return True
