"""
Database dependency registrations.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)
from app.infrastructure.persistence.database.engine import (
    get_session_factory,
)
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


class DatabaseProvider:
    """
    Provides database dependencies.
    """

    def __init__(
        self,
        settings: DatabaseSettings,
    ) -> None:

        self._session_factory: async_sessionmaker[
            AsyncSession
        ] = get_session_factory(settings)

    def session(
        self,
    ) -> AsyncSession:
        """
        Creates a new database session.
        """

        return self._session_factory()

    def unit_of_work(
        self,
    ) -> SqlAlchemyUnitOfWork:
        """
        Creates a new Unit of Work.
        """

        return SqlAlchemyUnitOfWork(
            self.session(),
        )