from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    # Database settings
    db_dialect: str = "postgresql"
    db_driver: str = "asyncpg"
    db_hostname: str = "postgresql"
    db_username: str = Field(default_factory=str, alias="POSTGRES_USER")
    db_password: str = Field(default_factory=str, alias="POSTGRES_PASSWORD")
    db_name: str = Field(default_factory=str, alias="POSTGRES_DB")


settings: Settings = Settings()
