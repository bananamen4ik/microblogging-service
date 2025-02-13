"""
Main entry point for the FastAPI application.

This module initializes the FastAPI app.
It is the starting point for running the application
and serves as the core interface for incoming requests.
"""

from contextlib import asynccontextmanager

from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.routers import users
from app.crud.base import init_db
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler
)


@asynccontextmanager
async def lifespan(_=None) -> AsyncGenerator[None, None]:
    """
    Initialize and shut down the FastAPI application.

    This context manager handles the setup and cleanup tasks when the FastAPI
    application starts and stops.
    """
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
