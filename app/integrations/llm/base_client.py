"""
Base LLM Client
"""

from abc import ABC, abstractmethod

from app.integrations.llm.response import LLMResponse


class BaseLLMClient(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """
        Generate a response from an LLM.
        """
        raise NotImplementedError