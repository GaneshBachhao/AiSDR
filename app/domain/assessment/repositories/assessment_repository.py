# app/domain/assessment/repositories/assessment_repository.py

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.discovery.identifiers.discovery_id import (
    DiscoveryId,
)


class AssessmentRepository(ABC):
    """
    Repository contract for the Assessment aggregate.

    This contract belongs to the Domain layer.

    Repository implementations are provided by the
    Infrastructure layer.
    """

    @abstractmethod
    async def save(
        self,
        assessment: Assessment,
    ) -> Assessment:
        """
        Persist an assessment.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        assessment_id: AssessmentId,
    ) -> Assessment | None:
        """
        Retrieve an assessment by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_discovery(
        self,
        discovery_id: DiscoveryId,
    ) -> Assessment | None:
        """
        Retrieve the assessment associated with a
        discovery.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        assessment_id: AssessmentId,
    ) -> bool:
        """
        Determine whether an assessment exists.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        assessment: Assessment,
    ) -> None:
        """
        Remove an assessment.
        """
        raise NotImplementedError