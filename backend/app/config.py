from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CampusOS API"
    environment: str = "development"
    api_prefix: str = "/api"
    database_url: str = "postgresql+asyncpg://campusos:campusos@localhost:5432/campusos"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
