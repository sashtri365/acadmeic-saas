from functools import lru_cache

from pydantic import model_validator
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
    redis_url: str | None = None
    login_rate_limit: int = 10
    login_rate_window_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_security_settings(self) -> "Settings":
        if self.environment == "production":
            if not self.database_url:
                raise ValueError("DATABASE_URL is required in production")
            if not self.jwt_secret or len(self.jwt_secret) < 32:
                raise ValueError("JWT_SECRET must be at least 32 characters in production")
            if not self.redis_url:
                raise ValueError("REDIS_URL is required in production")
            if not self.secure_cookies:
                raise ValueError("SECURE_COOKIES must be true in production")
            if "*" in self.allowed_hosts or "*" in self.cors_origins:
                raise ValueError("wildcard hosts/origins are forbidden in production")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
