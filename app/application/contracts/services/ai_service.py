from abc import ABC, abstractmethod

from app.domain.ai.entities.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse


class AIService(ABC):
    """
    AI generation service contract.
    """

    @abstractmethod
    async def generate(
        self,
        request: AIRequest
    ) -> AIResponse:
        pass