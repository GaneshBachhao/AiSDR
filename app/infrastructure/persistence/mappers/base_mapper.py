"""
Generic Domain <-> ORM mapper.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
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
        Convert domain object into persistence-safe dictionary.

        Converts domain identifiers:
            CompanyId
            LeadId
            ContactId

        into UUID values.
        """

        if is_dataclass(domain):
            data = asdict(domain)
        elif hasattr(domain, "__dict__"):
            data = {
                key: value
                for key, value in vars(domain).items()
                if not key.startswith("_")
            }
        else:
            raise TypeError(
                f"Unsupported domain object type: {type(domain).__name__}"
            )

        return BaseMapper._normalize_values(data)

    @staticmethod
    def _normalize_values(
        value: Any,
    ) -> Any:
        """
        Convert domain specific values into database values.
        """

        if isinstance(value, dict):
            return {
                key: BaseMapper._normalize_values(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                BaseMapper._normalize_values(item)
                for item in value
            ]

        if hasattr(value, "value"):
            return value.value

        return value

    @staticmethod
    def model_to_dict(
        model: Any,
    ) -> dict[str, Any]:
        """
        Convert SQLAlchemy model into dictionary.
        """

        return {
            column.key: getattr(model, column.key)
            for column in inspect(model).mapper.column_attrs
        }

    @staticmethod
    def copy_matching_fields(
        source: dict[str, Any],
        destination_type: type,
    ) -> dict[str, Any]:
        """
        Returns only keys existing on destination model.
        """

        try:
            fields = {
                column.key
                for column in inspect(
                    destination_type
                ).mapper.column_attrs
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