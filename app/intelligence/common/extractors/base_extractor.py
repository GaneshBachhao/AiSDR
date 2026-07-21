"""
Base Extractor

Shared functionality for all intelligence extractors.
"""

from abc import ABC
from abc import abstractmethod

from app.intelligence.common.schemas.evidence_schema import (
    Evidence,
)


class BaseExtractor(ABC):
    """
    Base class for all extractors.
    """

    DEFAULT_CONFIDENCE = 0.90

    DEFAULT_WEIGHT = 1.0

    @abstractmethod
    def extract(
        self,
        text: str,
    ) -> list[Evidence]:
        """
        Extract evidence from text.
        """
        raise NotImplementedError

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize input.
        """

        return text.lower().strip()

    def build_evidence(
        self,
        *,
        category: str,
        source: str,
        text: str,
        confidence: float | None = None,
        weight: float | None = None,
    ) -> Evidence:

        return Evidence(

            category=category,

            source=source,

            text=text,

            confidence=confidence
            if confidence is not None
            else self.DEFAULT_CONFIDENCE,

            weight=weight
            if weight is not None
            else self.DEFAULT_WEIGHT,
        )