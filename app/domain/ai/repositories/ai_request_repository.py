from abc import ABC, abstractmethod
from typing import List, Optional

from ..aggregate.ai_request import AIRequest
from ..value_objects.ai_request_id import AIRequestId


class AIRequestRepository(ABC):
    """
    Repository abstraction for AIRequest aggregates.
    """

    @abstractmethod
    def save(
        self,
        request: AIRequest,
    ) -> None:
        """
        Persist an AI request.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        request_id: AIRequestId,
    ) -> Optional[AIRequest]:
        """
        Retrieve an AI request by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[AIRequest]:
        """
        Retrieve all AI requests.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(
        self,
        request: AIRequest,
    ) -> None:
        """
        Remove an AI request.
        """
        raise NotImplementedError