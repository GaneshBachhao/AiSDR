"""
Central registry for Domain <-> Persistence conversions.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.domain.shared.identifiers.identifier import Identifier


class ConverterRegistry:
    """Convert domain value objects at the persistence boundary."""

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
        self._to_database[value_object_type] = to_database
        self._to_domain[value_object_type] = to_domain

    def to_database(self, value: Any) -> Any:
        if value is None:
            return None

        # Strong identifiers are persisted as their UUID values.
        if isinstance(value, Identifier):
            return value.value

        for registered_type, converter in self._to_database.items():
            if isinstance(value, registered_type):
                return converter(value)

        return value

    def to_domain(self, value_object_type: Any, value: Any) -> Any:
        if value is None:
            return None

        converter = self._to_domain.get(value_object_type)
        if converter is not None:
            return converter(value)

        if isinstance(value_object_type, type):
            for registered_type, converter in self._to_domain.items():
                if issubclass(value_object_type, registered_type):
                    return converter(value)

        return value


converter_registry = ConverterRegistry()

# Registration side effects.
from . import converters as _converters  # noqa: F401,E402
