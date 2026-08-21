from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.domain.ai.entities.ai_response import AIResponse
from app.domain.lead.enums.reply_classification import ReplyClassification
from app.infrastructure.ai.exceptions.ai_rate_limit_exception import AIRateLimitException
from app.infrastructure.lead.ai_reply_classification_adapter import (
    AiReplyClassificationAdapter,
)


def _ai_service(content: str | None = None, side_effect=None):
    service = AsyncMock()
    if side_effect is not None:
        service.execute.side_effect = side_effect
    else:
        service.execute.return_value = AIResponse(content=content)
    return service


@pytest.mark.asyncio
async def test_parses_a_valid_classification_response():
    ai_service = _ai_service(content='{"classification": "Interested", "confidence": "HIGH"}')
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    result = await adapter.classify("Sounds great, let's set up a call.")

    assert result.classification == ReplyClassification.INTERESTED
    assert result.confidence == "HIGH"


@pytest.mark.asyncio
async def test_strips_markdown_code_fences_before_parsing():
    ai_service = _ai_service(
        content='```json\n{"classification": "Unsubscribe", "confidence": "MEDIUM"}\n```'
    )
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    result = await adapter.classify("Please remove me from this list.")

    assert result.classification == ReplyClassification.UNSUBSCRIBE
    assert result.confidence == "MEDIUM"


@pytest.mark.asyncio
async def test_falls_back_to_not_now_low_on_malformed_json():
    ai_service = _ai_service(content="not valid json at all")
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    result = await adapter.classify("whatever")

    assert result.classification == ReplyClassification.NOT_NOW
    assert result.confidence == "LOW"


@pytest.mark.asyncio
async def test_falls_back_to_not_now_low_on_unknown_classification_value():
    ai_service = _ai_service(content='{"classification": "Angry", "confidence": "HIGH"}')
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    result = await adapter.classify("whatever")

    assert result.classification == ReplyClassification.NOT_NOW
    assert result.confidence == "LOW"


@pytest.mark.asyncio
async def test_falls_back_to_not_now_low_on_ai_exception():
    ai_service = _ai_service(side_effect=RuntimeError("provider unavailable"))
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    result = await adapter.classify("whatever")

    assert result.classification == ReplyClassification.NOT_NOW
    assert result.confidence == "LOW"


@pytest.mark.asyncio
async def test_defaults_unrecognized_confidence_to_low():
    ai_service = _ai_service(content='{"classification": "Objection", "confidence": "SURE"}')
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    result = await adapter.classify("Too expensive for us right now.")

    assert result.classification == ReplyClassification.OBJECTION
    assert result.confidence == "LOW"


@pytest.mark.asyncio
async def test_propagates_ai_rate_limit_instead_of_falling_back():
    """A rate limit means this reply was never actually classified -- it
    must not be indistinguishable from a genuine NOT_NOW read."""
    ai_service = _ai_service(side_effect=AIRateLimitException("Gemini rate limit / quota exceeded"))
    adapter = AiReplyClassificationAdapter(ai_service=ai_service)

    with pytest.raises(AIRateLimitException):
        await adapter.classify("whatever")


@pytest.mark.asyncio
async def test_defaults_to_gemini_provider_and_its_configured_model(monkeypatch):
    import app.infrastructure.lead.ai_reply_classification_adapter as module

    monkeypatch.setattr(module, "default_model_for_provider", lambda name: f"default-{name}")
    ai_service = _ai_service(content='{"classification": "OutOfOffice", "confidence": "HIGH"}')

    adapter = AiReplyClassificationAdapter(ai_service=ai_service)
    await adapter.classify("I am out of office until Monday.")

    sent_request = ai_service.execute.await_args.args[0]
    assert sent_request.provider.value == "gemini"
    assert sent_request.model.value == "default-gemini"


@pytest.mark.asyncio
async def test_provider_and_model_are_configurable():
    ai_service = _ai_service(content='{"classification": "WrongPerson", "confidence": "HIGH"}')

    adapter = AiReplyClassificationAdapter(
        ai_service=ai_service,
        provider_name="openai",
        model_name="gpt-4.1",
    )
    await adapter.classify("I'm not the right person for this.")

    sent_request = ai_service.execute.await_args.args[0]
    assert sent_request.provider.value == "openai"
    assert sent_request.model.value == "gpt-4.1"
