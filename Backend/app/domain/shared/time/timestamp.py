from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Timestamp:
    """
    Represents a UTC timestamp in the domain.
    """

    value: datetime

    def __post_init__(self) -> None:
        """
        Validate timestamp timezone.
        """
        if self.value.tzinfo is None:
            raise ValueError("Timestamp must contain timezone information.")

    @classmethod
    def now(cls) -> Timestamp:
        """
        Create current UTC timestamp.
        """
        return cls(datetime.now(UTC))

    def __str__(self) -> str:
        return self.value.isoformat()
