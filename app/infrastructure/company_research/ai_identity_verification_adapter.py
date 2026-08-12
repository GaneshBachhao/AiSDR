"""
AI-assisted implementation of ``IdentityVerificationPort``.

This is the fix for the defect the port exists to prevent: a candidate
named "Lathangi Motors Private Limited" must never be resolved to
"tatamotors.com" merely because both strings contain the word "motors".
Deterministic substring/token matching cannot reliably tell same-word
companies apart from each other, or a subsidiary from its unrelated-parent
domain -- so this adapter gathers Tavily evidence about the candidate and
asks an LLM (via the shared ``AIExecutionService``) to reason over that
evidence and decide, in structured form, whether it genuinely supports the
match.

The underlying AI provider (Gemini, OpenAI, or Azure OpenAI) is a
configuration choice, not a code choice -- ``AIExecutionService`` already
routes by ``AIRequest.provider``, so this adapter only needs the provider
name and a model/deployment name, both supplied by the composition root
(see ``app.presentation.api.dependencies.company_research``).

Every failure path (no Tavily evidence, no AI provider configured, a
malformed/unparseable AI response, an AI exception) resolves to
``confidence="LOW"`` and ``verified_website=None``. This adapter must never
silently upgrade an unverified guess to a confirmed match.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re

from pydantic import ValidationError

from app.application.ai.services.ai_execution_service import AIExecutionService
from app.application.company_research.ports.identity_verification_port import (
    IdentityVerificationPort,
    IdentityVerificationResult,
)
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.infrastructure.ai.composition import default_model_for_provider
from app.integrations.tavily.tavily_client import AgneticTavilyClient

logger = logging.getLogger(__name__)

_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


class AiIdentityVerificationAdapter(IdentityVerificationPort):
    """Verifies a candidate's identity and official website using Tavily + an LLM."""

    def __init__(
        self,
        ai_service: AIExecutionService,
        tavily_client: AgneticTavilyClient | None = None,
        provider_name: str = "gemini",
        model_name: str | None = None,
    ) -> None:
        self._ai_service = ai_service
        self._client = tavily_client or AgneticTavilyClient()
        self._provider = provider_name
        self._model = model_name or default_model_for_provider(provider_name)

    async def verify(self, candidate: CompanyCandidate) -> IdentityVerificationResult:
        try:
            evidence_items = await asyncio.to_thread(self._search_evidence, candidate)
            if not evidence_items and not candidate.content:
                return _unverified("no_public_evidence_found")

            prompt = self._build_prompt(candidate, evidence_items)
            response = await self._ai_service.execute(
                AIRequest(
                    provider=ProviderName(self._provider),
                    model=ModelName(self._model),
                    prompt=Prompt(prompt),
                    temperature=Temperature(0.1),
                    max_tokens=MaxTokens(1024),
                )
            )

            parsed = self._parse_json(response.content)
            return self._to_result(parsed)

        except Exception as exc:
            root_cause = exc
            while root_cause.__cause__ is not None:
                root_cause = root_cause.__cause__
            logger.warning(
                "Identity verification failed for %r: %s (root cause: %s: %s)",
                candidate.company_name,
                exc,
                type(root_cause).__name__,
                root_cause,
            )
            return _unverified(f"identity_verification_error: {exc}")

    def _search_evidence(self, candidate: CompanyCandidate) -> list[dict]:
        query = (
            f'"{candidate.company_name}" "{candidate.website or ""}" '
            "company official website industry headquarters employees parent company"
        )
        return self._client.search(query=query, max_results=5, search_depth="basic")

    @staticmethod
    def _build_prompt(candidate: CompanyCandidate, evidence_items: list[dict]) -> str:
        lines = []
        for item in evidence_items[:5]:
            title = str(item.get("title", "")).strip()
            url = str(item.get("url", "")).strip()
            snippet = str(item.get("content", "")).strip()[:300]
            if title or url:
                lines.append(f"- {title} ({url}): {snippet}")
        evidence_block = "\n".join(lines) if lines else "(no public evidence found)"

        return (
            "You are verifying whether a discovered company record genuinely "
            "corresponds to a real, distinct company and a specific website.\n\n"
            f'Candidate company name: "{candidate.company_name}"\n'
            f"Candidate proposed website: {candidate.website or 'unknown'}\n"
            f"Candidate page title: {candidate.title}\n"
            f"Candidate page snippet: {candidate.content[:500]}\n\n"
            "Public web evidence gathered about this candidate:\n"
            f"{evidence_block}\n\n"
            "Task: Decide if the evidence clearly shows that THIS EXACT company "
            "(not a different company that merely shares a word in its name, and "
            "not an unrelated parent/conglomerate) genuinely operates the proposed "
            "website.\n\n"
            "Rules:\n"
            "- Do not match based on partial word overlap alone (e.g. \"Lathangi "
            'Motors" is NOT "Tata Motors" even though both contain "Motors").\n'
            "- If the evidence is ambiguous, insufficient, or points to a "
            "different or larger company, set is_match to false and confidence "
            "to LOW.\n"
            "- Only set confidence to HIGH when the evidence explicitly and "
            "unambiguously ties this company name to this website.\n"
            "- If the company appears to be a subsidiary of a larger/parent "
            "company, name the parent in parent_company.\n\n"
            "Respond with ONLY a single-line JSON object, no markdown, no "
            "explanation, in exactly this shape:\n"
            '{"is_match": true or false, "confidence": "HIGH" or "MEDIUM" or '
            '"LOW", "verified_website": "https://..." or null, "parent_company": '
            '"..." or null, "reason": "short reason"}'
        )

    @staticmethod
    def _parse_json(content: str) -> dict:
        cleaned = _JSON_FENCE.sub("", content.strip()).strip()
        return json.loads(cleaned)

    @staticmethod
    def _to_result(parsed: dict) -> IdentityVerificationResult:
        is_match = bool(parsed.get("is_match"))
        confidence = str(parsed.get("confidence", "LOW")).strip().upper()
        if confidence not in {"HIGH", "MEDIUM", "LOW"}:
            confidence = "LOW"

        website = parsed.get("verified_website") if is_match else None
        reason = str(parsed.get("reason") or "no_reason_provided").strip()

        if not is_match:
            website = None
            confidence = "LOW" if confidence == "HIGH" else confidence

        try:
            return IdentityVerificationResult(
                verified_website=website or None,
                confidence=confidence,
                parent_company=(parsed.get("parent_company") or None),
                reason=reason,
            )
        except ValidationError:
            return _unverified(f"invalid_website_from_model: {website!r}")


def _unverified(reason: str) -> IdentityVerificationResult:
    return IdentityVerificationResult(
        verified_website=None,
        confidence="LOW",
        parent_company=None,
        reason=reason,
    )
