"""Schemas for users."""

from pydantic import BaseModel, ConfigDict

from app.schemas.base import ResultResponse


class UserBase(BaseModel):
    """
    Base schema with main config and attrs.

    Attributes:
        name (str): Full name.
    """

    name: str

    model_config = ConfigDict(from_attributes=True)


class UserInCreate(UserBase):
    """
    Schema for validating input data when creating a new user.

    Attributes:
        api_key (str): The API key, used for authentication.
    """

    api_key: str


class UserSchema(UserBase):
    """
    Schema for user.

    Attributes:
        id (int): Database id.
        api_key (str): The API key, used for authentication.
    """

    id: int
    api_key: str


class UserFollowers(BaseModel):
    """
    Schema for user followers representation.

    id (int): User id.
    name (str): Username.
    """

    id: int
    name: str


class UserFollowing(BaseModel):
    """
    Schema for user following representation.

    id (int): User id.
    name (str): Username.
    """

    id: int
    name: str


class UserOut(BaseModel):
    """
    Schema for profile representation.

    id (int): User id.
    name (str): Username.
    followers (list[UserFollowers]): User followers.
    following (list[UserFollowing]): User following.
    """

    id: int
    name: str
    followers: list[UserFollowers]
    following: list[UserFollowing]


class UserGetProfileResponse(ResultResponse):
    """Schema for get profile response."""

    user: UserOut
