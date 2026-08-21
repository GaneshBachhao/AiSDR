"""
AI-assisted implementation of ``ReplyClassificationPort``.

Mirrors ``AiIdentityVerificationAdapter``'s JSON-mode-by-convention shape
(hand-built prompt, fenced-JSON strip, ``json.loads``) rather than inventing
new AI-calling conventions. A rate-limit failure propagates distinctly (the
caller needs to know the classification was never actually attempted); any
other failure -- a provider error, a malformed/unparseable response, or a
category outside the six allowed values -- degrades to the safe, most
conservative sentinel (``NOT_NOW``/``LOW``) rather than a 500. NOT_NOW is the
right sentinel here (not, say, UNSUBSCRIBE or WRONG_PERSON) because it is the
one classification whose Lead-status/score/sequence effects are the least
destructive to get wrong.
"""

from __future__ import annotations

import json
import logging
import re

from app.application.ai.services.ai_execution_service import AIExecutionService
from app.application.lead.ports.reply_classification_port import (
    ReplyClassificationPort,
    ReplyClassificationResult,
)
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.lead.enums.reply_classification import ReplyClassification
from app.infrastructure.ai.composition import default_model_for_provider
from app.infrastructure.ai.exceptions.ai_rate_limit_exception import AIRateLimitException

logger = logging.getLogger(__name__)

_JSON_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)

_CATEGORY_DEFINITIONS = (
    '"Interested" - genuinely wants to learn more, asks questions, requests '
    "a call/demo/next steps.\n"
    '"NotNow" - polite decline for now, bad timing, revisit later, no ask '
    "to stop contacting.\n"
    '"Objection" - pushes back on price/fit/need but engages with the '
    "substance rather than declining outright.\n"
    '"Unsubscribe" - explicitly asks to stop being contacted / opt out.\n'
    '"OutOfOffice" - an automated out-of-office/vacation auto-responder, '
    "not a real reply from the person.\n"
    '"WrongPerson" - the recipient says this isn\'t their role/responsibility '
    "or they're the wrong contact."
)

_SENTINEL = ReplyClassificationResult(
    classification=ReplyClassification.NOT_NOW,
    confidence="LOW",
)


class AiReplyClassificationAdapter(ReplyClassificationPort):
    """Classifies reply text into one of six categories using an LLM."""

    def __init__(
        self,
        ai_service: AIExecutionService,
        provider_name: str = "gemini",
        model_name: str | None = None,
    ) -> None:
        self._ai_service = ai_service
        self._provider = provider_name
        self._model = model_name or default_model_for_provider(provider_name)

    async def classify(self, reply_text: str) -> ReplyClassificationResult:
        try:
            response = await self._ai_service.execute(
                AIRequest(
                    provider=ProviderName(self._provider),
                    model=ModelName(self._model),
                    prompt=Prompt(self._build_prompt(reply_text)),
                    temperature=Temperature(0.1),
                    max_tokens=MaxTokens(200),
                )
            )
            parsed = self._parse_json(response.content)
            return self._to_result(parsed)

        except AIRateLimitException:
            # Let a rate limit propagate distinctly instead of folding it
            # into the sentinel -- "never actually classified because the
            # provider was rate-limited" must stay visibly different from
            # "classified and genuinely landed on NotNow."
            raise
        except Exception as exc:
            logger.warning("Reply classification failed: %s", exc)
            return _SENTINEL

    @staticmethod
    def _build_prompt(reply_text: str) -> str:
        return (
            "You are classifying a sales prospect's email/LinkedIn reply "
            "into exactly one category.\n\n"
            f"Reply text:\n{reply_text}\n\n"
            "Categories:\n"
            f"{_CATEGORY_DEFINITIONS}\n\n"
            "Respond with ONLY a single-line JSON object, no markdown, no "
            "explanation, in exactly this shape:\n"
            '{"classification": "Interested" or "NotNow" or "Objection" or '
            '"Unsubscribe" or "OutOfOffice" or "WrongPerson", "confidence": '
            '"HIGH" or "MEDIUM" or "LOW"}'
        )

    @staticmethod
    def _parse_json(content: str) -> dict:
        cleaned = _JSON_FENCE.sub("", content.strip()).strip()
        return json.loads(cleaned)

    @staticmethod
    def _to_result(parsed: dict) -> ReplyClassificationResult:
        raw_classification = str(parsed.get("classification", "")).strip()
        try:
            classification = ReplyClassification(raw_classification)
        except ValueError:
            return _SENTINEL

        confidence = str(parsed.get("confidence", "LOW")).strip().upper()
        if confidence not in {"HIGH", "MEDIUM", "LOW"}:
            confidence = "LOW"

        return ReplyClassificationResult(classification=classification, confidence=confidence)
