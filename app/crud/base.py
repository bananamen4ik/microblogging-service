from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import (
    follows,
    likes,
    medias,
    tweets,
    users
)
from app.database import (
    engine,
    Base
)


async def init_db() -> None:
    connection: AsyncConnection

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
