"""
SQLAlchemy implementation of Unit of Work.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.infrastructure.persistence.repositories.ai.sqlalchemy_ai_request_repository import (
    SQLAlchemyAIRequestRepository,
)

from .base_unit_of_work import BaseUnitOfWork


class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    """
    SQLAlchemy transactional Unit of Work.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:

        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":

        self._session = self._session_factory()

        self.ai_requests = SQLAlchemyAIRequestRepository(
            self._session,
        )

        return self

    async def commit(
        self,
    ) -> None:

        await self._session.commit()

    async def rollback(
        self,
    ) -> None:

        await self._session.rollback()

    async def close(
        self,
    ) -> None:

        await self._session.close()