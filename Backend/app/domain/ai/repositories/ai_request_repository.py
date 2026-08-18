from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.value_objects.ai_request_id import AIRequestId


class AIRequestRepository(ABC):
    """
    Repository interface for AIRequest aggregate.
    """

    @abstractmethod
    async def save(
        self,
        request: AIRequest,
    ) -> AIRequest:
        """
        Persist an AI request.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        request_id: AIRequestId,
    ) -> AIRequest | None:
        """
        Retrieve an AI request.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        request_id: AIRequestId,
    ) -> bool:
        """
        Determine whether the request exists.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        request: AIRequest,
    ) -> None:
        """
        Remove an AI request.
        """
        raise NotImplementedError
