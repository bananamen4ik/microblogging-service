from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool

    # Database settings
    db_dialect: str = "postgresql"
    db_driver: str = "asyncpg"
    db_hostname: str = "postgresql"
    db_username: str = Field(alias="POSTGRES_USER")
    db_password: str = Field(alias="POSTGRES_PASSWORD")
    db_name: str = Field(alias="POSTGRES_DB")


settings: Settings = Settings()
