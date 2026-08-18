from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Evidence:
    """
    Represents supporting evidence for a finding.

    Evidence provides objective information that justifies
    a business finding.
    """

    title: str

    description: str

    source: str

    reference: str | None = None

    evidence_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """

        if not self.title.strip():
            raise ValueError("Evidence title cannot be empty.")

        if not self.description.strip():
            raise ValueError("Evidence description cannot be empty.")

        if not self.source.strip():
            raise ValueError("Evidence source cannot be empty.")
