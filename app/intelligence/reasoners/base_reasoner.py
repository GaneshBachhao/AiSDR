"""
Base Reasoner

Base class for all enterprise reasoners.
"""

from abc import ABC
from abc import abstractmethod

from app.intelligence.common.schemas import (
    IntelligenceReport,
)


class BaseReasoner(ABC):
    """
    Base reasoner.
    """

    @abstractmethod
    def reason(
        self,
        report: IntelligenceReport,
    ) -> list:
        """
        Generate business insights.
        """
        raise NotImplementedError