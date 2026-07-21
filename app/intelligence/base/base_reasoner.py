"""
Base Reasoner

Shared base class for all AI BDOS reasoning engines.
"""

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseReasoner(
    ABC,
    Generic[InputT, OutputT],
):
    """
    Base class for all AI BDOS reasoning engines.
    """

    # ------------------------------------------------------------------
    # Reasoner Metadata
    # ------------------------------------------------------------------

    name: str = "BaseReasoner"
    version: str = "1.0.0"
    description: str = ""

    @property
    def reasoner_type(self) -> str:
        """
        Returns the concrete reasoner type.
        """
        return self.__class__.__name__

    # ------------------------------------------------------------------
    # Reasoning
    # ------------------------------------------------------------------

    @abstractmethod
    def reason(
        self,
        data: InputT,
    ) -> OutputT:
        """
        Produce reasoning.
        """
        raise NotImplementedError