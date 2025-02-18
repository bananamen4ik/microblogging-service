"""Schemas for tweets."""

from pydantic import BaseModel, ConfigDict


class TweetBase(BaseModel):
    """
    Base schema with main config and attrs.

    Attributes:
        user_id (int): User id owner.
        main_content (str): Main content.
        medias (list[int] | None): Medias ids.
    """

    user_id: int
    main_content: str
    medias: list[int] | None = None

    model_config = ConfigDict(from_attributes=True)


class TweetIn(TweetBase):
    """Schema for tweet create."""


class TweetSchema(TweetBase):
    """
    Main schema for tweet.

    Attributes:
        id (int): Tweet id.
    """

    id: int
