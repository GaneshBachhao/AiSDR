from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.discovery.enums.response_type import ResponseType


@dataclass
class DiscoveryResponse:
    """
    Represents a response captured during a discovery session.

    This entity is owned by DiscoverySession and does not exist
    independently.
    """

    question_id: str

    question: str

    answer: str

    response_type: ResponseType = ResponseType.TEXT

    confidence: float = 1.0

    remarks: str | None = None

    response_id: UUID = field(
        default_factory=uuid4
    )


    def __post_init__(self) -> None:

        if not self.question_id.strip():
            raise ValueError(
                "Question ID cannot be empty."
            )

        if not self.question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not self.answer.strip():
            raise ValueError(
                "Answer cannot be empty."
            )

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Confidence must be between 0 and 1."
            )