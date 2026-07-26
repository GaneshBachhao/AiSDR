"""
Infrastructure dependency providers.

Provides application dependencies for the Presentation layer.
"""

from __future__ import annotations

from functools import lru_cache

from app.infrastructure.configuration.database_settings import (
    DatabaseSettings,
)
from app.infrastructure.dependency_injection.container import (
    Container,
)
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)


@lru_cache
def get_container() -> Container:
    """
    Return the application's singleton container.
    """

    settings = DatabaseSettings()

    return Container(
        settings=settings,
    )


def get_unit_of_work() -> SqlAlchemyUnitOfWork:
    """
    Create a new Unit of Work.
    """

    return get_container().create_unit_of_work()