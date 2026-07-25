"""
Infrastructure dependency container.
"""

from __future__ import annotations

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)
from app.infrastructure.dependency_injection.database import (
    DatabaseProvider,
)
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


class Container:
    """
    Root infrastructure container.
    """

    def __init__(
        self,
        settings: DatabaseSettings,
    ) -> None:

        self.database = DatabaseProvider(
            settings,
        )

    def create_unit_of_work(
        self,
    ) -> SqlAlchemyUnitOfWork:
        """
        Create SQLAlchemy Unit of Work.
        """

        return SqlAlchemyUnitOfWork(
            self.database.session(),
        )