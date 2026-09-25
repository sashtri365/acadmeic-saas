from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CampusOS API"
    environment: str = "development"
    api_prefix: str = "/api"
    database_url: str | None = None
    allowed_hosts: str = "localhost,127.0.0.1"
    cors_origins: str = "http://localhost:3000"
    jwt_secret: str | None = None
    access_token_minutes: int = 15
    refresh_token_days: int = 7
    secure_cookies: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
