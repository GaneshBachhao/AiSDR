"""
Database configuration settings.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """
    SQLAlchemy database configuration.
    """

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        extra="ignore",
    )

    database_url: str | None = None

    driver: str = "postgresql+asyncpg"

    username: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    database: str = "aisdr"

    echo: bool = False

    pool_size: int = 10
    max_overflow: int = 20
    pool_recycle: int = 1800