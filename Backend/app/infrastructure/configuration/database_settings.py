"""
Database configuration settings.
"""

from __future__ import annotations

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class DatabaseSettings(BaseSettings):
    """
    SQLAlchemy database configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    database_url: str = "sqlite+aiosqlite:///./aisdr.db"

    driver: str = "sqlite+aiosqlite"

    username: str | None = None

    password: str | None = None

    host: str | None = None

    port: int | None = None

    database: str = "aisdr.db"

    echo: bool = False

    pool_size: int = 5

    max_overflow: int = 10

    pool_recycle: int = 1800
