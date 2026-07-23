import pytest

from app.infrastructure.ai.configuration import (
    ProviderSettings,
)

from app.infrastructure.ai.factories import (
    AIProviderFactory,
)

from app.infrastructure.ai.providers import (
    OpenAIProvider,
    AzureOpenAIProvider,
    GeminiProvider,
    MockProvider,
)


def test_factory_creates_openai_provider():

    settings = ProviderSettings(
        provider_name="openai",
        api_key="test-key",
    )

    provider = AIProviderFactory.create(
        settings
    )

    assert isinstance(
        provider,
        OpenAIProvider,
    )


def test_factory_creates_azure_openai_provider():

    settings = ProviderSettings(
        provider_name="azure_openai",
        api_key="test-key",
        endpoint="test-endpoint",
    )

    provider = AIProviderFactory.create(
        settings
    )

    assert isinstance(
        provider,
        AzureOpenAIProvider,
    )


def test_factory_creates_gemini_provider():

    settings = ProviderSettings(
        provider_name="gemini",
        api_key="test-key",
    )

    provider = AIProviderFactory.create(
        settings
    )

    assert isinstance(
        provider,
        GeminiProvider,
    )


def test_factory_creates_mock_provider():

    settings = ProviderSettings(
        provider_name="mock",
    )

    provider = AIProviderFactory.create(
        settings
    )

    assert isinstance(
        provider,
        MockProvider,
    )


def test_factory_rejects_unknown_provider():

    settings = ProviderSettings(
        provider_name="unknown",
        api_key="test-key",
    )


    with pytest.raises(
        ValueError
    ):

        AIProviderFactory.create(
            settings
        )