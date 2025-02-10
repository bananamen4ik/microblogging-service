from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError

from ..schemas.users import UserInCreate, UserOutCreate

from ..models import User


async def get_user(api_key: str):
    ...


async def create_user(session: AsyncSession, user: UserInCreate) -> UserOutCreate | None:
    try:
        new_user: User = User(**user.model_dump())

        session.add(new_user)
        await session.commit()

        return UserOutCreate.model_validate(new_user)
    except IntegrityError:
        return None
