from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.value_objects.assessment_id import (
    AssessmentId,
)
from app.domain.discovery.value_objects.discovery_id import (
    DiscoveryId,
)


class AssessmentRepository(ABC):
    """
    Repository interface for the Assessment aggregate.
    """

    @abstractmethod
    def save(
        self,
        assessment: Assessment,
    ) -> Assessment:
        """
        Persist an assessment.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        assessment_id: AssessmentId,
    ) -> Assessment | None:
        """
        Retrieve an assessment by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_discovery(
        self,
        discovery_id: DiscoveryId,
    ) -> Assessment | None:
        """
        Retrieve an assessment associated with a discovery session.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        assessment_id: AssessmentId,
    ) -> bool:
        """
        Check whether an assessment exists.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        assessment: Assessment,
    ) -> None:
        """
        Remove an assessment.
        """
        raise NotImplementedError