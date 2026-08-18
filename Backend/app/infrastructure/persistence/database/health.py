"""
Database health checks.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.engine import (
    get_async_engine,
)


@dataclass(slots=True, frozen=True)
class DatabaseHealthStatus:
    """
    Represents the database health.
    """

    healthy: bool
    database: str
    driver: str
    message: str


class DatabaseHealthChecker:
    """
    Performs database connectivity checks.
    """

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self._engine = get_async_engine(settings)

    async def check(self) -> DatabaseHealthStatus:
        """
        Executes a lightweight database health check.
        """

        try:
            async with self._engine.connect() as connection:
                await connection.execute(text("SELECT 1"))

            return DatabaseHealthStatus(
                healthy=True,
                database=self._settings.database,
                driver=self._settings.driver,
                message="Database connection successful.",
            )

        except SQLAlchemyError as ex:
            return DatabaseHealthStatus(
                healthy=False,
                database=self._settings.database,
                driver=self._settings.driver,
                message=str(ex),
            )

        except Exception as ex:
            return DatabaseHealthStatus(
                healthy=False,
                database=self._settings.database,
                driver=self._settings.driver,
                message=str(ex),
            )


async def database_health_check(
    settings: DatabaseSettings,
) -> DatabaseHealthStatus:
    """
    Dependency helper.
    """

    checker = DatabaseHealthChecker(settings)

    return await checker.check()
