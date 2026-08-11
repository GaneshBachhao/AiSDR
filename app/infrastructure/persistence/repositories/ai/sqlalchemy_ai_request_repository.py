"""
SQLAlchemy implementation of AIRequestRepository.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ai.aggregates.ai_request import AIRequest

from app.infrastructure.persistence.mappers.ai_request_mapper import (
    AIRequestMapper,
)

from app.infrastructure.persistence.models.ai_request_model import (
    AIRequestModel,
)

from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyAIRequestRepository(
    SqlAlchemyRepository[
        AIRequest,
        AIRequestModel,
        str,
    ],
):
    """
    SQLAlchemy implementation of AI Request repository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            session=session,
            mapper=AIRequestMapper(),
        )