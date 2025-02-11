from urllib import parse as urllib_parse

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    """ Base class for sqlalchemy models """


engine: AsyncEngine = create_async_engine(
    "{dialect}+{driver}://{username}:{password}@{hostname}/{dbname}".format(
        dialect=settings.db_dialect,
        driver=settings.db_driver,
        username=settings.db_username,
        password=urllib_parse.quote_plus(settings.db_password),
        hostname=settings.db_hostname,
        dbname=settings.db_name
    ),
    echo=settings.debug
)

async_session: async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
