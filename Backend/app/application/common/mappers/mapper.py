# app/application/common/mappers/mapper.py

"""
Mapper contract.

Application mappers transform data between Domain objects
and Application DTOs.

Concrete implementations belong to feature modules.

Example:

    LeadMapper
        Lead Entity
            ↕
        LeadResponseDTO
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TSource = TypeVar(
    "TSource",
)

TDestination = TypeVar(
    "TDestination",
)


class Mapper(
    ABC,
    Generic[TSource, TDestination],
):
    """
    Base mapper contract.
    """

    @abstractmethod
    def to_dto(
        self,
        source: TSource,
    ) -> TDestination:
        """
        Convert domain object to DTO.
        """
        raise NotImplementedError

    @abstractmethod
    def to_entity(
        self,
        target: TDestination,
    ) -> TSource:
        """
        Convert DTO to domain object.
        """
        raise NotImplementedError