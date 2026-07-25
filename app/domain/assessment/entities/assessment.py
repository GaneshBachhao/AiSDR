from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.assessment.value_objects.evidence import Evidence
from app.domain.assessment.entities.finding import Finding
from app.domain.assessment.enums.assessment_status import AssessmentStatus
from app.domain.assessment.enums.maturity_level import MaturityLevel
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.assessment.value_objects.assessment_score import AssessmentScore
from app.domain.assessment.value_objects.opportunity import Opportunity
from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Assessment(AggregateRoot[AssessmentId]):
    """
    Aggregate root representing the AI readiness assessment.
    """

    id: AssessmentId = field(
        default_factory=AssessmentId,
        kw_only=True,
    )

    discovery_session_id: DiscoverySessionId

    status: AssessmentStatus = AssessmentStatus.CREATED

    started_at: datetime | None = None

    completed_at: datetime | None = None

    score: AssessmentScore = field(
        default_factory=AssessmentScore,
    )

    maturity_level: MaturityLevel = MaturityLevel.INITIAL

    summary: str | None = None

    findings: list[Finding] = field(
        default_factory=list,
    )

    evidence: list[Evidence] = field(
        default_factory=list,
    )

    opportunities: list[Opportunity] = field(
        default_factory=list,
    )

    def start(self) -> None:
        """
        Start assessment.
        """
        self.status = AssessmentStatus.IN_PROGRESS
        self.started_at = datetime.now(UTC)
        self.touch()

    def complete(
        self,
        summary: str | None = None,
    ) -> None:
        """
        Complete assessment.
        """
        self.status = AssessmentStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.summary = summary
        self.touch()

    def update_score(
        self,
        score: AssessmentScore,
    ) -> None:
        """
        Update assessment score.
        """
        self.score = score
        self.touch()

    def update_maturity(
        self,
        maturity: MaturityLevel,
    ) -> None:
        """
        Update maturity level.
        """
        self.maturity_level = maturity
        self.touch()

    def add_finding(
        self,
        finding: Finding,
    ) -> None:
        """
        Add finding.
        """
        self.findings.append(finding)
        self.touch()

    def add_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        """
        Add supporting evidence.
        """
        self.evidence.append(evidence)
        self.touch()

    def add_opportunity(
        self,
        opportunity: Opportunity,
    ) -> None:
        """
        Add business opportunity.
        """
        self.opportunities.append(opportunity)
        self.touch()