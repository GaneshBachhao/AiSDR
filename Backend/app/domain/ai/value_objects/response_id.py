from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ResponseId:
    """
    Strongly typed identifier for AIResponse.
    """

    value: UUID = field(
        default_factory=uuid4,
    )

    def __str__(self) -> str:
        return str(self.value)