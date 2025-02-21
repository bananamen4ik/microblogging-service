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


class TweetAuthor(BaseModel):
    """
    Schema for tweet author representation.

    Attributes:
        id (int): Tweet author id.
        name (str): Tweet author name.
    """

    id: int
    name: str


class TweetLike(BaseModel):
    """
    Schema for tweet likes representation.

    Attributes:
        user_id (int): User id like owner.
        name (int): Name like owner.
    """

    user_id: int
    name: str


class TweetOut(BaseModel):
    """
    Schema for get tweets.

    Attributes:
        id (int): Tweet id.
        content (str): Tweet content text.
        attachments (list[str]): Tweet media links.
        author (TweetAuthor): Tweet author.
        likes (list[TweetLikes]): All tweet likes.
    """

    id: int
    content: str  # noqa: WPS110
    attachments: list[str] = []
    author: TweetAuthor
    likes: list[TweetLike] = []
