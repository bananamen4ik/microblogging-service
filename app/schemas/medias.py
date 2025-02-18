"""Schemas for medias."""

from pydantic import BaseModel, ConfigDict


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
    tweet_id: int | None

    model_config = ConfigDict(from_attributes=True)


class MediaSchema(MediaBase):
    """
    Main schema for media.

    Attributes:
        id (int): Media id.
    """

    id: int
