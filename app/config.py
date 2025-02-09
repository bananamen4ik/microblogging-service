from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool

    # Database settings
    db_dialect: str = "postgresql"
    db_driver: str = "asyncpg"
    db_hostname: str = "postgresql"
    db_username: str
    db_password: str
    db_name: str


settings: Settings = Settings()
