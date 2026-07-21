# app/application/common/interfaces/unit_of_work.py

"""
Unit of Work application contract.

Infrastructure implementations manage actual transactions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """
    Transaction boundary contract.

    Application services use this abstraction without knowing
    the underlying database technology.
    """

    @abstractmethod
    async def __aenter__(
        self,
    ) -> UnitOfWork:
        """
        Begin transaction scope.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        """
        End transaction scope.
        """
        raise NotImplementedError

    @abstractmethod
    async def commit(
        self,
    ) -> None:
        """
        Commit transaction.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(
        self,
    ) -> None:
        """
        Rollback transaction.
        """
        raise NotImplementedError