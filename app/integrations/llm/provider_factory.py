"""
LLM Provider Factory

Returns the configured Large Language Model client.
"""

from app.core.config import settings

from app.integrations.llm.base_client import (
    BaseLLMClient,
)

from app.integrations.llm.gemini_client import (
    GeminiClient,
)


class LLMProviderFactory:
    """
    Factory responsible for returning
    the configured LLM client.
    """

    @staticmethod
    def get_client() -> BaseLLMClient:

        provider = getattr(
            settings,
            "LLM_PROVIDER",
            "gemini",
        ).lower()

        if provider == "gemini":
            return GeminiClient()

        raise ValueError(
            f"Unsupported LLM Provider: {provider}"
        )