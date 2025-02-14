"""Test exceptions module."""

import json

import pytest

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import (
    http_exception_handler,
    validation_exception_handler
)
from app.tests.testing_utils import LOOP_SCOPE_SESSION


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_http_exception_handler() -> None:
    """
    Client and Starlette exceptions.

    This is for client errors, invalid authentication, invalid data, etc.
    AND if any part of Starlette's internal code,
    or a Starlette extension or plug-in, raises a Starlette HTTPException.
    """
    json_response: JSONResponse = await http_exception_handler(
        None,
        StarletteHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error"
        )
    )

    assert isinstance(json_response, JSONResponse)

    body_data: dict = json.loads(json_response.body)
    assert isinstance(body_data["result"], bool)
    assert body_data["error_type"] == StarletteHTTPException.__name__
    assert isinstance(body_data["error_message"], str)


@pytest.mark.asyncio(loop_scope=LOOP_SCOPE_SESSION)
async def test_validation_exception_handler() -> None:
    """API validation exception."""
    json_response: JSONResponse = await validation_exception_handler(
        None,
        RequestValidationError([{"msg": ""}])
    )

    assert isinstance(json_response, JSONResponse)

    body_data: dict = json.loads(json_response.body)
    assert isinstance(body_data["result"], bool)
    assert body_data["error_type"] == RequestValidationError.__name__
    assert isinstance(body_data["error_message"], str)
