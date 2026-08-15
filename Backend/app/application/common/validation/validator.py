# app/application/common/validation/validator.py

"""
Validator contract.

Concrete validators belong to individual application
use cases.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.application.common.validation.validation_result import (
    ValidationResult,
)


TRequest = TypeVar(
    "TRequest",
)


class Validator(
    ABC,
    Generic[TRequest],
):
    """
    Base application validator contract.
    """

    @abstractmethod
    async def validate(
        self,
        request: TRequest,
    ) -> ValidationResult:
        """
        Validate application request.
        """
        raise NotImplementedError