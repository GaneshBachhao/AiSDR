"""
Database context helpers.

Provides request-scoped database session handling.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)
from app.infrastructure.persistence.database.session import (
    get_session_manager,
)


class DatabaseContext:
    """
    Wraps an AsyncSession for request-scoped database operations.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    @property
    def session(
        self,
    ) -> AsyncSession:
        """
        Returns the active AsyncSession.
        """

        return self._session

    async def commit(
        self,
    ) -> None:
        await self._session.commit()

    async def rollback(
        self,
    ) -> None:
        await self._session.rollback()

    async def flush(
        self,
    ) -> None:
        await self._session.flush()

    async def refresh(
        self,
        entity: object,
    ) -> None:
        await self._session.refresh(
            entity,
        )

    async def close(
        self,
    ) -> None:
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

    manager = get_session_manager(
        settings,
    )

    session = manager.create_session()

    try:

        yield DatabaseContext(
            session,
        )

    finally:

        await session.close()