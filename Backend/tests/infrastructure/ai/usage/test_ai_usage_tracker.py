from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.ai.value_objects.token_usage import TokenUsage
from app.infrastructure.ai.usage.ai_usage_tracker import AIUsageTracker


class _FakeSessionManager:
    """Test double bound directly to the in-memory test engine, bypassing
    the real (process-global-singleton) DatabaseSessionManager entirely."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def create_session(self):
        return self._factory()


def _request(provider: str = "gemini", model: str = "gemini-3.5-flash") -> AIRequest:
    return AIRequest(
        provider=ProviderName(provider),
        model=ModelName(model),
        prompt=Prompt("hello"),
        temperature=Temperature(0.1),
        max_tokens=MaxTokens(50),
    )


@pytest.mark.asyncio
async def test_log_persists_a_completed_request(engine):
    tracker = AIUsageTracker(session_manager=_FakeSessionManager(engine))
    request = _request()
    request.start()
    request.complete(
        AIResponse(
            content="ok",
            finish_reason=FinishReason.STOP,
            token_usage=TokenUsage(prompt_tokens=5, completion_tokens=3),
        )
    )

    await tracker.log(request)

    assert await tracker.count_requests_today("gemini") == 1


@pytest.mark.asyncio
async def test_log_persists_a_failed_request(engine):
    tracker = AIUsageTracker(session_manager=_FakeSessionManager(engine))
    request = _request()
    request.start()
    request.fail("boom")

    await tracker.log(request)

    # A failed call still consumed quota against the provider.
    assert await tracker.count_requests_today("gemini") == 1


@pytest.mark.asyncio
async def test_count_requests_today_is_scoped_per_provider(engine):
    tracker = AIUsageTracker(session_manager=_FakeSessionManager(engine))

    gemini_request = _request(provider="gemini")
    gemini_request.start()
    gemini_request.complete(AIResponse(content="ok", finish_reason=FinishReason.STOP))
    await tracker.log(gemini_request)

    openai_request = _request(provider="openai", model="gpt-4.1")
    openai_request.start()
    openai_request.complete(AIResponse(content="ok", finish_reason=FinishReason.STOP))
    await tracker.log(openai_request)

    assert await tracker.count_requests_today("gemini") == 1
    assert await tracker.count_requests_today("openai") == 1
    assert await tracker.count_requests_today("azure_openai") == 0


@pytest.mark.asyncio
async def test_count_requests_today_accumulates_multiple_calls(engine):
    tracker = AIUsageTracker(session_manager=_FakeSessionManager(engine))

    for _ in range(3):
        request = _request()
        request.start()
        request.complete(AIResponse(content="ok", finish_reason=FinishReason.STOP))
        await tracker.log(request)

    assert await tracker.count_requests_today("gemini") == 3


@pytest.mark.asyncio
async def test_log_swallows_persistence_errors():
    class _BrokenSessionManager:
        def create_session(self):
            raise RuntimeError("db unavailable")

    tracker = AIUsageTracker(session_manager=_BrokenSessionManager())
    request = _request()
    request.start()
    request.complete(AIResponse(content="ok", finish_reason=FinishReason.STOP))

    # Must not raise -- logging failures can never break the underlying AI call.
    await tracker.log(request)
