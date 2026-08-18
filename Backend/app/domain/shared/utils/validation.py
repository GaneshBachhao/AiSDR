from __future__ import annotations

import re
from uuid import UUID


class Validation:
    """
    Common domain validation utilities.

    This class contains reusable technical validations.
    Business rules should remain inside aggregates
    and value objects.
    """

    @staticmethod
    def required(
        value: str,
        field_name: str,
    ) -> None:
        """
        Validate required text values.
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required.")

    @staticmethod
    def max_length(
        value: str,
        length: int,
        field_name: str,
    ) -> None:
        """
        Validate maximum string length.
        """
        if len(value) > length:
            raise ValueError(f"{field_name} cannot exceed {length} characters.")

    @staticmethod
    def range(
        value: float,
        minimum: float,
        maximum: float,
        field_name: str,
    ) -> None:
        """
        Validate numeric range.
        """
        if not minimum <= value <= maximum:
            raise ValueError(f"{field_name} must be between {minimum} and {maximum}.")

    @staticmethod
    def positive(
        value: float,
        field_name: str,
    ) -> None:
        """
        Validate positive numbers.
        """
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative.")

    @staticmethod
    def valid_uuid(
        value: UUID,
        field_name: str,
    ) -> None:
        """
        Validate UUID values.
        """
        if not isinstance(value, UUID):
            raise ValueError(f"{field_name} must be a valid UUID.")

    @staticmethod
    def valid_email(
        email: str,
    ) -> None:
        """
        Basic email format validation.
        """
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, email):
            raise ValueError("Invalid email format.")
