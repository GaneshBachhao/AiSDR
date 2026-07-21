"""
Base Classifier

Shared base class for all AI BDOS classifiers.
"""

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class BaseClassifier(
    ABC,
    Generic[InputT, OutputT],
):
    """
    Base class for all AI BDOS classifiers.
    """

    # ------------------------------------------------------------------
    # Classifier Metadata
    # ------------------------------------------------------------------

    name: str = "BaseClassifier"
    version: str = "1.0.0"
    description: str = ""

    @property
    def classifier_type(self) -> str:
        """
        Returns the concrete classifier type.
        """
        return self.__class__.__name__

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    @abstractmethod
    def classify(
        self,
        data: InputT,
    ) -> OutputT:
        """
        Perform classification.
        """
        raise NotImplementedError