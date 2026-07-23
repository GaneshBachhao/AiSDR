import pytest

from app.infrastructure.ai.configuration import (
    ProviderSettings,
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

    
    assert isinstance(
        
        OpenAIProvider,
    )


def test_factory_creates_azure_openai_provider():

    settings = ProviderSettings(
        provider_name="azure_openai",
        api_key="test-key",
        endpoint="test-endpoint",
    )

  

    assert isinstance(
        
        AzureOpenAIProvider,
    )


def test_factory_creates_gemini_provider():

    settings = ProviderSettings(
        provider_name="gemini",
        api_key="test-key",
    )

  

    assert isinstance(
        
        GeminiProvider,
    )


def test_factory_creates_mock_provider():

    settings = ProviderSettings(
        provider_name="mock",
    )

   

    assert isinstance(
        
        MockProvider,
    )

 