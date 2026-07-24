"""
SQLAlchemy async session management.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.engine import (
    get_session_factory,
)


class SessionManager:
    """
    Manages SQLAlchemy AsyncSession instances.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Creates a managed AsyncSession.
        """

        session = self._session_factory()

        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise

        finally:
            await session.close()

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Executes a transactional scope.
        """

        async with self.session() as session:
            async with session.begin():
                yield session


_session_manager: SessionManager | None = None


def get_session_manager(
    settings: DatabaseSettings,
) -> SessionManager:
    """
    Returns singleton SessionManager.
    """

    global _session_manager

    if _session_manager is None:
        _session_manager = SessionManager(
            get_session_factory(settings)
        )

    return _session_manager


async def get_db_session(
    settings: DatabaseSettings,
) -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency.

    Example:

        Depends(get_db_session)
    """

    manager = get_session_manager(settings)

    async with manager.session() as session:
        yield session