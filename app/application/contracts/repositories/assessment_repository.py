from abc import ABC, abstractmethod

from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.value_objects.assessment_id import AssessmentId


class AssessmentRepository(ABC):
    """
    Assessment persistence contract.
    """

    @abstractmethod
    async def add(
        self,
        assessment: Assessment
    ) -> None:
        pass

    @abstractmethod
    async def get_by_id(
        self,
        assessment_id: AssessmentId
    ) -> Assessment | None:
        pass

    @abstractmethod
    async def update(
        self,
        assessment: Assessment
    ) -> None:
        pass