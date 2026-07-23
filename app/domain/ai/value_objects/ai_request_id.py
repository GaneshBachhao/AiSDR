from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class AIRequestId:
    """
    Strongly typed identifier for AIRequest aggregate.
    """

    value: UUID = field(
        default_factory=uuid4,
    )

    def __str__(self) -> str:
        return str(self.value)