from sqlalchemy.ext.asyncio import AsyncConnection

from app.models import follows  # noqa: F401
from app.models import likes  # noqa: F401
from app.models import medias  # noqa: F401
from app.models import tweets  # noqa: F401
from app.models import users  # noqa: F401

from app.database import (
    engine,
    Base
)


async def init_db() -> None:
    connection: AsyncConnection

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
