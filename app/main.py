from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import settings

from .routers import users

from .crud.base import init_db

from .exceptions import (
    http_exception_handler,
    validation_exception_handler
)


@asynccontextmanager
async def lifespan(_):
    await init_db()
    yield


app: FastAPI = FastAPI(
    lifespan=lifespan,
    debug=settings.debug,
    exception_handlers={
        StarletteHTTPException: http_exception_handler,
        RequestValidationError: validation_exception_handler
    }
)

app.include_router(users.router)
