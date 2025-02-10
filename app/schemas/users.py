from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class UserInCreate(UserBase):
    api_key: str


class UserOutCreate(UserInCreate):
    id: int
