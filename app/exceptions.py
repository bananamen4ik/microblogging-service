from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(_, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": str(type(exc).__name__),
            "error_message": str(exc.detail)
        }
    )


async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    error: dict = exc.errors()[0]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "result": False,
            "error_type": str(type(exc).__name__),
            "error_message": "{}: {}".format(
                error["msg"],
                error["loc"][1]
            )
        }
    )
