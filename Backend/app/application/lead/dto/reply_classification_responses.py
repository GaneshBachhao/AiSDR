"""Reply classification response DTO (EPIC-10.1/10.3)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ReplyClassificationResponseDTO:
    """Outcome of classifying a reply and applying it to the Lead."""

    classification: str
    confidence: str
    lead_status: str
    lead_score: int
    sequences_stopped: list[str] = field(default_factory=list)
