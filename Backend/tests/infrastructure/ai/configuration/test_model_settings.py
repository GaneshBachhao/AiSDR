import pytest

from app.infrastructure.ai.configuration import ModelSettings


def test_create_model_settings():

    model = ModelSettings(
        model_name="gpt-4o",
        max_tokens=4096,
        temperature=0.5,
    )

    assert model.model_name == "gpt-4o"
    assert model.max_tokens == 4096
    assert model.temperature == 0.5


def test_invalid_temperature():

    with pytest.raises(ValueError):
        ModelSettings(
            model_name="gpt",
            temperature=3,
        )


def test_invalid_max_tokens():

    with pytest.raises(ValueError):
        ModelSettings(
            model_name="gpt",
            max_tokens=0,
        )


def test_capability_lookup():

    model = ModelSettings(
        model_name="gpt",
        capabilities=[
            "chat",
            "vision",
        ],
    )

    assert model.supports_capability("chat")
    assert not model.supports_capability("audio")
