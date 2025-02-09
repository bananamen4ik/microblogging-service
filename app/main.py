from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings

from .routers import users

from .crud.base import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    debug=settings.debug
)

app.include_router(users.router)
