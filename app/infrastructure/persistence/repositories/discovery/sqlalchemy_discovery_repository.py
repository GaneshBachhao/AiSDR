"""
SQLAlchemy implementation of DiscoveryRepository.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.discovery.entities.discovery import Discovery
from app.infrastructure.persistence.mappers.discovery_mapper import (
    DiscoveryMapper,
)
from app.infrastructure.persistence.models.discovery_model import (
    DiscoveryModel,
)
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyDiscoveryRepository(
    SqlAlchemyRepository[
        Discovery,
        DiscoveryModel,
        str,
    ],
):
    """
    SQLAlchemy Discovery repository.
    """

    model_type = DiscoveryModel
    mapper = DiscoveryMapper()

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        super().__init__(
            session=session,
            mapper=self.mapper,
        )