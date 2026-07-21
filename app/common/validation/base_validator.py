"""
Base Validator

Shared validation contract for all AI BDOS validators.
"""

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from common.validation.validation_result import ValidationResult


InputT = TypeVar("InputT")


class BaseValidator(
    ABC,
    Generic[InputT],
):
    """
    Base class for all AI BDOS validators.
    """

    # ------------------------------------------------------------------
    # Validator Metadata
    # ------------------------------------------------------------------

    name: str = "BaseValidator"
    version: str = "1.0.0"
    description: str = ""

    @property
    def validator_type(self) -> str:
        """
        Returns the concrete validator type.
        """
        return self.__class__.__name__

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        value: InputT,
    ) -> ValidationResult[InputT]:
        """
        Validate the supplied value.

        Parameters
        ----------
        value
            Value to validate.

        Returns
        -------
        ValidationResult
            Validation outcome.
        """
        raise NotImplementedError