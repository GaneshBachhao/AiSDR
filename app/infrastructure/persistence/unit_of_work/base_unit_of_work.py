"""
Base Unit of Work contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseUnitOfWork(ABC):
    """
    Coordinates repositories and transaction boundaries.
    """

    async def __aenter__(self) -> "BaseUnitOfWork":
        return self

    @abstractmethod
    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
        """
        Exit Unit of Work.
        """

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit current transaction.
        """

    @abstractmethod
    async def rollback(self) -> None:
        """
        Rollback current transaction.
        """