"""
SQLAlchemy implementation of AssessmentRepository.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.assessment.entities.assessment import Assessment
from app.infrastructure.persistence.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.infrastructure.persistence.models.assessment_model import (
    AssessmentModel,
)
from app.infrastructure.persistence.repositories.base.sqlalchemy_repository import (
    SqlAlchemyRepository,
)


class SqlAlchemyAssessmentRepository(
    SqlAlchemyRepository[
        Assessment,
        AssessmentModel,
        str,
    ],
):

    model_type = AssessmentModel
    mapper = AssessmentMapper()

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(session)