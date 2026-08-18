import pytest

from app.infrastructure.ai.configuration import (
    AISettings,
    ModelSettings,
    ProviderSettings,
)


def create_settings() -> AISettings:

    return AISettings(
        default_provider="openai",
        providers={
            "openai": ProviderSettings(
                provider_name="openai",
                api_key="secret",
            ),
        },
        models={
            "gpt-4o": ModelSettings(
                model_name="gpt-4o",
            ),
        },
    )


def test_create_ai_settings():

    settings = create_settings()

    assert settings.default_provider == "openai"


def test_get_provider():

    settings = create_settings()

    provider = settings.get_provider(
        "openai",
    )

    assert provider.provider_name == "openai"


def test_get_model():

    settings = create_settings()

    model = settings.get_model(
        "gpt-4o",
    )

    assert model.model_name == "gpt-4o"


def test_unknown_provider():

    settings = create_settings()

    with pytest.raises(ValueError):
        settings.get_provider(
            "gemini",
        )


def test_unknown_model():

    settings = create_settings()

    with pytest.raises(ValueError):
        settings.get_model(
            "unknown",
        )


def test_default_provider_must_exist():

    with pytest.raises(ValueError):
        AISettings(
            default_provider="gemini",
            providers={
                "openai": ProviderSettings(
                    provider_name="openai",
                    api_key="secret",
                ),
            },
            models={},
        )
