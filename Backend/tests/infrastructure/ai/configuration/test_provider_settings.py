import pytest

from app.infrastructure.ai.configuration import ProviderSettings


def test_create_provider_settings():

    settings = ProviderSettings(
        provider_name="openai",
        api_key="secret",
    )

    assert settings.provider_name == "openai"
    assert settings.api_key == "secret"
    assert settings.enabled is True


def test_mock_provider_does_not_require_api_key():

    settings = ProviderSettings(
        provider_name="mock",
    )

    assert settings.is_mock_provider


def test_enabled_provider_requires_api_key():

    with pytest.raises(ValueError):
        ProviderSettings(
            provider_name="openai",
        )


def test_provider_name_required():

    with pytest.raises(ValueError):
        ProviderSettings(
            provider_name="",
            api_key="secret",
        )
