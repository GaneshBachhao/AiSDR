# app/domain/discovery/identifiers/discovery_session_id.py

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DiscoverySessionId:
    """
    Strongly typed identifier for DiscoverySession aggregates.
    """

    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)