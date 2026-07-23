from abc import ABC, abstractmethod

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse

class BaseAIProvider(ABC):
    """
    Base contract for AI providers.

    All AI providers must implement
    this interface.
    """


    @abstractmethod
    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute AI request.
        """

        pass


    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check provider availability.
        """

        pass