"""Schemas for medias."""

from pydantic import BaseModel, ConfigDict

from app.schemas.base import ResultResponse


class MediaBase(BaseModel):
    """
    Base schema with main config and attrs.

    Attributes:
        ext (str): Media extension without dot.
        user_id (int): User id owner.
        tweet_id (int | None): Tweet id.
    """

    ext: str
    user_id: int
    tweet_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class MediaSchema(MediaBase):
    """
    Main schema for media.

    Attributes:
        id (int): Media id.
    """

    id: int


class MediaUploadImageResponse(ResultResponse):
    """Schema for upload image API response."""

    media_id: int
