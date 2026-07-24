"""
Database context helpers.

Provides request-scoped session handling and transactional execution.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.session import (
    get_session_manager,
)


class DatabaseContext:
    """
    Encapsulates a request-scoped database session.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """
        Returns the active AsyncSession.
        """
        return self._session

    async def commit(self) -> None:
        """
        Commit pending changes.
        """
        await self._session.commit()

    async def rollback(self) -> None:
        """
        Roll back pending changes.
        """
        await self._session.rollback()

    async def flush(self) -> None:
        """
        Flush pending changes.
        """
        await self._session.flush()

    async def refresh(self, entity: object) -> None:
        """
        Refresh an entity from the database.
        """
        await self._session.refresh(entity)

    async def close(self) -> None:
        """
        Close the current session.
        """
        await self._session.close()


@asynccontextmanager
async def database_context(
    settings: DatabaseSettings,
) -> AsyncGenerator[DatabaseContext, None]:
    """
    Creates a request-scoped DatabaseContext.

    Example:

        async with database_context(settings) as db:
            ...
    """

    manager = get_session_manager(settings)

    async with manager.session() as session:
        yield DatabaseContext(session)