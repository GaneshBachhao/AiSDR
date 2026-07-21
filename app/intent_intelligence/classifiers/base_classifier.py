"""
Base Classifier

Base class for all intent intelligence classifiers.
"""

from abc import ABC
from abc import abstractmethod


class BaseClassifier(ABC):
    """
    Base classifier.
    """

    @abstractmethod
    def classify(
        self,
        text: str,
    ):
        """
        Classify input text.
        """
        raise NotImplementedError