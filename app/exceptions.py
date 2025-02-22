"""Utility functions for handling custom exceptions."""

from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.exceptions import MainException


async def http_exception_handler(
        _,
        exc: StarletteHTTPException
) -> JSONResponse:
    """Exception handler StarletteHTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content=MainException(
            result=False,
            error_type=type(exc).__name__,
            error_message=exc.detail
        ).model_dump()
    )


async def validation_exception_handler(
        _,
        exc: RequestValidationError
) -> JSONResponse:
    """Exception handler RequestValidationError."""
    error: dict = exc.errors()[0]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=MainException(
            result=False,
            error_type=type(exc).__name__,
            error_message=error["msg"]
        ).model_dump()
    )
