from app.infrastructure.ai.clients import (
    OpenAIClient,
    AzureOpenAIClient,
    GeminiClient,
)

from app.infrastructure.ai.configuration import (
    ProviderSettings,
)

from app.infrastructure.ai.providers import (
    BaseAIProvider,
    OpenAIProvider,
    AzureOpenAIProvider,
    GeminiProvider,
    MockProvider,
)


class AIProviderFactory:
    """
    Factory responsible for creating AI providers.
    """


    @staticmethod
    def create(
        settings: ProviderSettings,
    ) -> BaseAIProvider:
        """
        Create AI provider based on configuration.
        """

        provider = settings.provider_name.lower()


        if provider == "openai":

            client = OpenAIClient(
                settings=settings
            )

            return OpenAIProvider(
                client=client,
                settings=settings,
            )


        if provider == "azure_openai":

            client = AzureOpenAIClient(
                settings=settings
            )

            return AzureOpenAIProvider(
                client=client,
                settings=settings,
            )


        if provider == "gemini":

            client = GeminiClient(
                settings=settings
            )

            return GeminiProvider(
                client=client,
                settings=settings,
            )


        if provider == "mock":

            return MockProvider()


        raise ValueError(
            f"Unsupported AI provider: {settings.provider_name}"
        )