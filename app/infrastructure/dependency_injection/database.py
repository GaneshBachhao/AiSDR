"""
Dependency Injection - Database.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.infrastructure.persistence.database import (
    create_engine,
    create_session_factory,
)

from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


class DatabaseContainer:
    """
    Creates database infrastructure.
    """

    def __init__(
        self,
        connection_string: str,
    ) -> None:

        self.engine = create_engine(
            connection_string,
        )

        self.session_factory: async_sessionmaker[
            AsyncSession
        ] = create_session_factory(
            self.engine,
        )

    def unit_of_work(
        self,
    ) -> SQLAlchemyUnitOfWork:

        return SQLAlchemyUnitOfWork(
            self.session_factory,
        )