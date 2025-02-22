"""Schemas for exceptions."""

from app.schemas.base import ResultResponse


class MainException(ResultResponse):
    """Schema for all exceptions."""

    error_type: str
    error_message: str
