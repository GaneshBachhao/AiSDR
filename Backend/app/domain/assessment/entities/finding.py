from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.assessment.value_objects.evidence import Evidence
from app.domain.assessment.enums.finding_type import FindingType


@dataclass
class Finding:
    """
    Represents a business finding identified during an assessment.

    A finding captures an observation, risk, gap, opportunity,
    strength, or recommendation hint derived from the discovery
    process.
    """

    title: str

    description: str

    finding_type: FindingType

    finding_id: UUID = field(default_factory=uuid4)

    severity: int = 3

    recommendation_hint: str | None = None

    evidence: list[Evidence] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Validate business invariants.
        """
        if not self.title.strip():
            raise ValueError(
                "Finding title cannot be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "Finding description cannot be empty."
            )

        if not 1 <= self.severity <= 5:
            raise ValueError(
                "Severity must be between 1 and 5."
            )

    def add_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        """
        Attach supporting evidence to this finding.
        """
        if evidence not in self.evidence:
            self.evidence.append(evidence)

    def remove_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        """
        Remove supporting evidence from this finding.
        """
        if evidence in self.evidence:
            self.evidence.remove(evidence)