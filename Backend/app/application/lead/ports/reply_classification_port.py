"""
Application port for classifying an inbound reply from a Lead's contact.

Six categories only (EPIC-10.1): interested / not now / objection /
unsubscribe / out of office / wrong person. A malformed or unparseable AI
response must degrade to a safe, conservative sentinel rather than fail the
request -- see ``AiReplyClassificationAdapter``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.lead.enums.reply_classification import ReplyClassification


@dataclass(frozen=True)
class ReplyClassificationResult:
    """Outcome of classifying one reply's text."""

    classification: ReplyClassification
    confidence: str  # "HIGH" | "MEDIUM" | "LOW"


class ReplyClassificationPort(ABC):
    """Application port for classifying a reply's text into a category."""

    @abstractmethod
    async def classify(self, reply_text: str) -> ReplyClassificationResult:
        """Classify ``reply_text`` into one of the six reply categories."""
        raise NotImplementedError
