"""Logic functionality with users."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import (
    get_user_by_id,
    add_follow as crud_add_follow
)
from app.models.users import User
from app.models.follows import Follow
from app.schemas.users import (
    UserOut,
    UserFollowers,
    UserFollowing
)


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


async def get_profile(user: User) -> UserOut:
    """Get profile."""
    followers: list[User] = await user.awaitable_attrs.followers_users
    followings: list[User] = await user.awaitable_attrs.following_users

    return UserOut(
        id=user.id,
        name=user.name,
        followers=[
            UserFollowers(
                id=follower.id,
                name=follower.name
            )
            for follower in followers
        ],
        following=[
            UserFollowing(
                id=following.id,
                name=following.name
            )
            for following in followings
        ]
    )
