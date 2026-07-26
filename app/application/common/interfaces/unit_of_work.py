"""
Unit of Work application contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self

from app.application.contracts.repositories.lead_repository import (
    LeadRepository,
)


class UnitOfWork(ABC):
    """
    Coordinates repositories within a transaction.
    """

    leads: LeadRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError