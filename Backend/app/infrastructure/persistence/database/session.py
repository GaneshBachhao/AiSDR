"""
Database session manager.

Owns the SQLAlchemy AsyncSession factory.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)
from app.infrastructure.persistence.database.engine import (
    get_database_engine,
)


class DatabaseSessionManager:
    """
    Creates AsyncSession instances using the shared engine.
    """

    def __init__(
        self,
        settings: DatabaseSettings,
    ) -> None:

        self._engine = get_database_engine(
            settings,
        )

        self._session_factory = async_sessionmaker(
            bind=self._engine.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def session_factory(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        """
        Returns the configured session factory.
        """

        return self._session_factory

    def create_session(
        self,
    ) -> AsyncSession:
        """
        Creates a new AsyncSession.
        """

        return self._session_factory()


_session_manager: DatabaseSessionManager | None = None


def get_session_manager(
    settings: DatabaseSettings,
) -> DatabaseSessionManager:
    """
    Returns the singleton session manager.
    """

    global _session_manager

    if _session_manager is None:

        _session_manager = DatabaseSessionManager(
            settings,
        )

    return _session_manager