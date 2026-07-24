"""
Database dependency registrations.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.engine import (
    get_session_factory,
)


class DatabaseProvider:
    """
    Provides database dependencies.
    """

    def __init__(
        self,
        settings: DatabaseSettings,
    ) -> None:
        self._session_factory = get_session_factory(settings)

    def session(self) -> AsyncSession:
        """
        Creates a new AsyncSession.
        """
        return self._session_factory()