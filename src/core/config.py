from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    VERSION: str = "1"
    API_PREFIX: str = f"/api/v{VERSION}"
    REDIS_DSN: RedisDsn
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
    CHAT_WEBHOOK_API_URL: AnyHttpUrl = "http://localhost:8000/api/v1/test"
    PROJECT_NAME: str = "mnovikov"
    ALLOWED_HOSTS: List[str] | None = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
