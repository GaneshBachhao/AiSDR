"""
Generic Domain <-> ORM mapper.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import asdict
from dataclasses import is_dataclass
from typing import Any
from typing import Generic
from typing import TypeVar

from sqlalchemy.inspection import inspect

TDomain = TypeVar("TDomain")
TModel = TypeVar("TModel")


class BaseMapper(Generic[TDomain, TModel], ABC):
    """
    Generic mapper between Domain entities and SQLAlchemy models.

    Subclasses only specify the concrete domain/model types.
    """

    domain_type: type[TDomain]
    model_type: type[TModel]

    @abstractmethod
    def to_domain(
        self,
        model: TModel,
    ) -> TDomain:
        """
        ORM -> Domain
        """

    @abstractmethod
    def to_model(
        self,
        domain: TDomain,
    ) -> TModel:
        """
        Domain -> ORM
        """

    @staticmethod
    def domain_to_dict(
        domain: Any,
    ) -> dict[str, Any]:
        """
        Convert a domain object into a dictionary.

        Supports dataclasses and regular Python objects.
        """

        if is_dataclass(domain):
            return asdict(domain)

        if hasattr(domain, "__dict__"):
            return {
                key: value
                for key, value in vars(domain).items()
                if not key.startswith("_")
            }

        raise TypeError(
            f"Unsupported domain object type: {type(domain).__name__}"
        )

    @staticmethod
    def model_to_dict(
        model: Any,
    ) -> dict[str, Any]:
        """
        Convert a SQLAlchemy model into a dictionary.
        """

        return {
            column.name: getattr(model, column.name)
            for column in inspect(model).mapper.column_attrs
        }

    @staticmethod
    def copy_matching_fields(
        source: dict[str, Any],
        destination_type: type,
    ) -> dict[str, Any]:
        """
        Returns only keys that exist on destination type.
        """

        try:
            fields = {
                column.key
                for column in inspect(destination_type).mapper.column_attrs
            }
        except Exception:
            fields = set(
                getattr(
                    destination_type,
                    "__annotations__",
                    {},
                ).keys()
            )

        return {
            key: value
            for key, value in source.items()
            if key in fields
        }