"""Schemas for common options."""

from pydantic import BaseModel


class ResultResponse(BaseModel):
    """Schema for result only response."""

    result: bool  # noqa: WPS110
