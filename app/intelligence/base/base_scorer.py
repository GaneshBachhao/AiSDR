"""
Base Scorer

Shared base class for all AI BDOS scorers.
"""

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

InputT = TypeVar("InputT")


class BaseScorer(
    ABC,
    Generic[InputT],
):
    """
    Base class for all AI BDOS scoring engines.
    """

    # ------------------------------------------------------------------
    # Scorer Metadata
    # ------------------------------------------------------------------

    name: str = "BaseScorer"
    version: str = "1.0.0"
    description: str = ""

    @property
    def scorer_type(self) -> str:
        """
        Returns the concrete scorer type.
        """
        return self.__class__.__name__

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    @abstractmethod
    def score(
        self,
        data: InputT,
    ) -> float:
        """
        Calculate a score.

        Returns
        -------
        float
            A normalized or domain-specific score.
        """
        raise NotImplementedError