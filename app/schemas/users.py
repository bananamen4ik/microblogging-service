"""Schemas for users."""

from pydantic import BaseModel, ConfigDict


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


class UserOutCreate(UserInCreate):
    """
    Schema for validating input data after creating a new user.

    Attributes:
        id (int): Database id.
    """

    id: int
