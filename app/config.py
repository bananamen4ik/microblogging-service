"""
Configuration settings for the application.

This module contains configuration values used by the application, including
settings for database connections, environment variables, and other system
settings.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

RESULT_KEY: str = "result"
HTTP_EXCEPTION_USER_API_KEY_INVALID: str = "The user was not found by api_key."


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class is responsible for loading and validating the configuration
    values from environment variables or default values. It uses Pydantic's
    BaseSettings to facilitate the management of application settings.
    """

    debug: bool = False
    path_images: Path = Path("/opt/images_volume")

    # Database settings
    db_dialect: str = "postgresql"
    db_driver: str = "asyncpg"
    db_hostname: str = "postgresql"
    db_username: str = Field(default="", alias="POSTGRES_USER")
    db_password: str = Field(default="", alias="POSTGRES_PASSWORD")
    db_name: str = Field(default="", alias="POSTGRES_DB")
    db_debug: bool = Field(default=False, alias="POSTGRES_DEBUG")


settings: Settings = Settings()
