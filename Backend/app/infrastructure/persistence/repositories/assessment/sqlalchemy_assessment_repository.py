"""
SQLAlchemy Assessment repository.

Architecture Freeze v5.0
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.repositories.assessment_repository import (
    AssessmentRepository as ApplicationAssessmentRepository,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.assessment.repositories.assessment_repository import (
    AssessmentRepository as DomainAssessmentRepository,
)
from app.domain.discovery.identifiers.discovery_id import (
    DiscoveryId,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)
from app.infrastructure.persistence.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.infrastructure.persistence.models.assessment_model import (
    AssessmentModel,
)
from app.infrastructure.persistence.models.discovery_model import (
    DiscoveryModel,
)


class SqlAlchemyAssessmentRepository(
    ApplicationAssessmentRepository,
    DomainAssessmentRepository,
):
    """
    SQLAlchemy implementation of Assessment repository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def add(
        self,
        assessment: Assessment,
    ) -> None:
        """
        Add assessment.
        """

        model = AssessmentMapper.to_model(
            assessment,
        )

        self._session.add(model)

        await self._session.flush()

    async def save(
        self,
        assessment: Assessment,
    ) -> Assessment:
        """
        Persist assessment and return the domain object.
        """

        existing = await self.get_by_id(
            assessment.id,
        )

        if existing is None:
            await self.add(
                assessment,
            )
        else:
            await self.update(
                assessment,
            )

        await self._session.flush()

        model = await self._session.get(
            AssessmentModel,
            assessment.id.value,
        )

        if model is None:
            raise ValueError(
                f"Assessment not found after save: {assessment.id.value}",
            )

        return AssessmentMapper.to_domain(model)

    async def get_by_id(
        self,
        assessment_id: AssessmentId,
    ) -> Assessment | None:
        """
        Retrieve assessment by identifier.
        """

        result = await self._session.execute(
            select(
                AssessmentModel,
            ).where(
                AssessmentModel.id == assessment_id.value,
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return AssessmentMapper.to_domain(model)

    async def get_by_discovery(
        self,
        discovery_id: DiscoveryId,
    ) -> Assessment | None:
        """
        Retrieve assessment by discovery identifier.
        """

        result = await self._session.execute(
            select(
                AssessmentModel,
            ).where(
                AssessmentModel.discovery_id == discovery_id.value,
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return AssessmentMapper.to_domain(model)

    async def get_by_lead_id(
        self,
        lead_id: LeadId,
    ) -> Assessment | None:
        """
        Retrieve assessment by lead identifier.
        """

        result = await self._session.execute(
            select(
                AssessmentModel,
            )
            .join(
                DiscoveryModel,
                DiscoveryModel.id == AssessmentModel.discovery_id,
            )
            .where(
                DiscoveryModel.lead_id == lead_id.value,
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return AssessmentMapper.to_domain(model)

    async def list(
        self,
        page: int = 1,
        page_size: int = 50,
        discovery_id: str | UUID | None = None,
    ) -> list[Assessment]:
        """
        List assessments with optional discovery filter.
        """

        safe_page = max(page, 1)
        safe_page_size = max(page_size, 1)

        offset = (safe_page - 1) * safe_page_size

        query = select(
            AssessmentModel,
        )

        if discovery_id is not None:
            query = query.where(
                AssessmentModel.discovery_id == UUID(str(discovery_id)),
            )

        result = await self._session.execute(query.offset(offset).limit(safe_page_size))

        return [AssessmentMapper.to_domain(model) for model in result.scalars().all()]

    async def update(
        self,
        assessment: Assessment,
    ) -> None:
        """
        Update assessment.
        """

        result = await self._session.execute(
            select(
                AssessmentModel,
            ).where(
                AssessmentModel.id == assessment.id.value,
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(
                f"Assessment not found: {assessment.id.value}",
            )

        AssessmentMapper.update_model(
            model,
            assessment,
        )

        await self._session.flush()

    async def delete(
        self,
        assessment: Assessment | AssessmentId,
    ) -> None:
        """
        Delete assessment.
        """

        assessment_id = assessment.id if isinstance(assessment, Assessment) else assessment

        result = await self._session.execute(
            select(
                AssessmentModel,
            ).where(
                AssessmentModel.id == assessment_id.value,
            )
        )

        model = result.scalar_one_or_none()

        if model is not None:
            await self._session.delete(model)

    async def exists(
        self,
        assessment_id: AssessmentId,
    ) -> bool:
        """
        Check whether an assessment exists.
        """

        result = await self._session.execute(
            select(
                AssessmentModel.id,
            ).where(
                AssessmentModel.id == assessment_id.value,
            )
        )

        return result.scalar_one_or_none() is not None
