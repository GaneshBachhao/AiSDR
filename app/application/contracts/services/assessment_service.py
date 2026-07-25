"""
Assessment service contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.assessment.entities.assessment import (
    Assessment,
)


class AssessmentService(ABC):
    """
    Assessment workflow contract.

    Application layer depends on this abstraction.
    """

    @abstractmethod
    async def execute(
        self,
        assessment: Assessment,
    ) -> Assessment:
        """
        Execute assessment workflow.
        """
        raise NotImplementedError