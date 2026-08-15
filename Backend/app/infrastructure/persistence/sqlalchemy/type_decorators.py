"""
Generic SQLAlchemy TypeDecorator implementations.

This module contains reusable infrastructure for mapping
Domain Value Objects to primitive database types.
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Generic, TypeVar

from sqlalchemy.types import TypeDecorator

TValueObject = TypeVar("TValueObject")


class ValueObjectType(TypeDecorator, Generic[TValueObject], ABC):
    """
    Generic SQLAlchemy converter for immutable Value Objects.

    Subclasses only need to define:

        impl = String / Integer / UUID / ...

        value_object = MyValueObject

    The Value Object must expose:

        .value

    and support construction as:

        MyValueObject(value)
    """

    cache_ok = True

    value_object: type[TValueObject]

    def process_bind_param(
        self,
        value: TValueObject | None,
        dialect: Any,
    ) -> Any:
        """
        Domain -> Database
        """

        if value is None:
            return None

        return value.value

    def process_result_value(
        self,
        value: Any,
        dialect: Any,
    ) -> TValueObject | None:
        """
        Database -> Domain
        """

        if value is None:
            return None

        return self.value_object(value)