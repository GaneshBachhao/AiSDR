from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.ai.entities.ai_response import AIResponse
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.infrastructure.company_research.ai_identity_verification_adapter import (
    AiIdentityVerificationAdapter,
)


def _lathangi_candidate() -> CompanyCandidate:
    return CompanyCandidate(
        company_name="Lathangi Motors Private Limited",
        website="https://tatamotors.com",
        title="Lathangi Motors",
        content="Lathangi Motors is a small dealership in Andhra Pradesh.",
        source_url="https://tatamotors.com",
    )


def _acme_candidate() -> CompanyCandidate:
    return CompanyCandidate(
        company_name="Acme Manufacturing",
        website="https://acme.example",
        title="Acme Manufacturing",
        content="Acme Manufacturing makes industrial parts.",
        source_url="https://acme.example",
    )


def _tavily_client(results):
    client = Mock()
    client.search.return_value = results
    return client


def _ai_service(content: str | None = None, side_effect=None):
    service = AsyncMock()
    if side_effect is not None:
        service.execute.side_effect = side_effect
    else:
        service.execute.return_value = AIResponse(content=content)
    return service


@pytest.mark.asyncio
async def test_rejects_same_word_unrelated_company_match():
    """The defect this port exists to fix: 'Motors' overlap must not create a false match."""
    client = _tavily_client(
        [{"title": "Tata Motors Official Site", "url": "https://tatamotors.com", "content": "Tata Motors is a large multinational automobile manufacturer."}]
    )
    ai_service = _ai_service(
        content='{"is_match": false, "confidence": "LOW", "verified_website": null, '
        '"parent_company": null, "reason": "Evidence describes an unrelated larger company."}'
    )
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_lathangi_candidate())

    assert result.verified_website is None
    assert result.confidence == "LOW"


@pytest.mark.asyncio
async def test_accepts_genuine_high_confidence_match():
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "Acme official site."}])
    ai_service = _ai_service(
        content='{"is_match": true, "confidence": "HIGH", "verified_website": "https://acme.example", '
        '"parent_company": null, "reason": "Official site explicitly matches candidate name."}'
    )
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_acme_candidate())

    assert str(result.verified_website).startswith("https://acme.example")
    assert result.confidence == "HIGH"


@pytest.mark.asyncio
async def test_strips_markdown_code_fences_before_parsing():
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(
        content='```json\n{"is_match": true, "confidence": "MEDIUM", "verified_website": '
        '"https://acme.example", "parent_company": null, "reason": "matched"}\n```'
    )
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_acme_candidate())
    assert result.confidence == "MEDIUM"


@pytest.mark.asyncio
async def test_falls_back_to_low_on_ai_exception():
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(side_effect=RuntimeError("provider unavailable"))
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_acme_candidate())

    assert result.confidence == "LOW"
    assert result.verified_website is None


@pytest.mark.asyncio
async def test_falls_back_to_low_on_malformed_json():
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(content="not valid json at all")
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_acme_candidate())

    assert result.confidence == "LOW"
    assert result.verified_website is None


@pytest.mark.asyncio
async def test_falls_back_to_low_on_invalid_website_url_from_model():
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(
        content='{"is_match": true, "confidence": "HIGH", "verified_website": "not-a-url", '
        '"parent_company": null, "reason": "matched"}'
    )
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_acme_candidate())

    assert result.confidence == "LOW"
    assert result.verified_website is None


@pytest.mark.asyncio
async def test_skips_ai_call_entirely_when_no_evidence_and_no_content():
    client = _tavily_client([])
    ai_service = _ai_service(content="{}")
    candidate = CompanyCandidate(company_name="Nobody Corp", website=None, title="", content="", source_url="")
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(candidate)

    assert result.confidence == "LOW"
    ai_service.execute.assert_not_called()


@pytest.mark.asyncio
async def test_never_returns_website_when_is_match_is_false_even_if_model_supplies_one():
    """Defensive: a model glitch that sets is_match=false but still fills verified_website must not leak through."""
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(
        content='{"is_match": false, "confidence": "HIGH", "verified_website": "https://acme.example", '
        '"parent_company": null, "reason": "inconsistent model output"}'
    )
    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    result = await adapter.verify(_acme_candidate())

    assert result.verified_website is None


@pytest.mark.asyncio
async def test_defaults_to_gemini_provider_and_its_configured_model(monkeypatch):
    import app.infrastructure.company_research.ai_identity_verification_adapter as module

    monkeypatch.setattr(module, "default_model_for_provider", lambda name: f"default-{name}")
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(content='{"is_match": false, "confidence": "LOW", "verified_website": null, "parent_company": null, "reason": "x"}')

    adapter = AiIdentityVerificationAdapter(ai_service=ai_service, tavily_client=client)

    await adapter.verify(_acme_candidate())

    sent_request = ai_service.execute.await_args.args[0]
    assert sent_request.provider.value == "gemini"
    assert sent_request.model.value == "default-gemini"


@pytest.mark.asyncio
async def test_provider_and_model_are_configurable():
    client = _tavily_client([{"title": "Acme", "url": "https://acme.example", "content": "x"}])
    ai_service = _ai_service(content='{"is_match": false, "confidence": "LOW", "verified_website": null, "parent_company": null, "reason": "x"}')

    adapter = AiIdentityVerificationAdapter(
        ai_service=ai_service,
        tavily_client=client,
        provider_name="openai",
        model_name="gpt-4.1",
    )

    await adapter.verify(_acme_candidate())

    sent_request = ai_service.execute.await_args.args[0]
    assert sent_request.provider.value == "openai"
    assert sent_request.model.value == "gpt-4.1"
