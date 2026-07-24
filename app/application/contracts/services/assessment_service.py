from abc import ABC, abstractmethod

from app.domain.assessment.entities.assessment import Assessment


class AssessmentService(ABC):
    """
    Assessment workflow contract.
    """

    @abstractmethod
    async def execute(
        self,
        assessment: Assessment
    ) -> Assessment:
        pass