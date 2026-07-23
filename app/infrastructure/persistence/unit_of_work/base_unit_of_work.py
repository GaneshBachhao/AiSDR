"""
Base Unit of Work contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.domain.ai.repositories.ai_request_repository import (
    AIRequestRepository,
)


class BaseUnitOfWork(ABC):
    """
    Defines a transactional boundary.
    """

    ai_requests: AIRequestRepository

    async def __aenter__(self) -> "BaseUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:

        if exc is None:
            await self.commit()
        else:
            await self.rollback()

        await self.close()

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit current transaction.
        """
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """
        Rollback current transaction.
        """
        ...

    @abstractmethod
    async def close(self) -> None:
        """
        Close underlying resources.
        """
        ...