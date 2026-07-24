"""
Central registry for Domain <-> Persistence conversions.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ConverterRegistry:
    """
    Registry responsible for converting Value Objects
    between Domain and Persistence representations.
    """

    def __init__(self) -> None:
        self._to_database: dict[type, Callable[[Any], Any]] = {}
        self._to_domain: dict[type, Callable[[Any], Any]] = {}

    def register(
        self,
        value_object_type: type,
        *,
        to_database: Callable[[Any], Any],
        to_domain: Callable[[Any], Any],
    ) -> None:
        """
        Register conversion functions.
        """

        self._to_database[value_object_type] = to_database
        self._to_domain[value_object_type] = to_domain

    def to_database(self, value: Any) -> Any:
        """
        Convert Domain -> Persistence.
        """

        if value is None:
            return None

        converter = self._to_database.get(type(value))

        if converter is None:
            return value

        return converter(value)

    def to_domain(
        self,
        value_object_type: type,
        value: Any,
    ) -> Any:
        """
        Convert Persistence -> Domain.
        """

        if value is None:
            return None

        converter = self._to_domain.get(value_object_type)

        if converter is None:
            return value

        return converter(value)


converter_registry = ConverterRegistry()