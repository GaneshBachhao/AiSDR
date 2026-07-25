from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.roadmap_phase import RoadmapPhase
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.enums.recommendation_status import (
    RecommendationStatus,
)
from app.domain.recommendation.identifiers.recommendation_id import (
    RecommendationId,
)
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Recommendation(AggregateRoot[RecommendationId]):
    """
    Aggregate root representing the AI recommendation
    generated from an assessment.
    """

    id: RecommendationId = field(
        default_factory=RecommendationId,
        kw_only=True,
    )

    assessment_id: AssessmentId

    status: RecommendationStatus = RecommendationStatus.DRAFT

    executive_summary: str | None = None

    submitted_at: datetime | None = None

    approved_at: datetime | None = None

    solutions: list[Solution] = field(
        default_factory=list,
    )

    roadmap_phases: list[RoadmapPhase] = field(
        default_factory=list,
    )

    def start(self) -> None:
        """
        Start recommendation creation.
        """
        self.status = RecommendationStatus.DRAFT
        self.touch()

    def add_solution(
        self,
        solution: Solution,
    ) -> None:
        """
        Add proposed solution.
        """
        self.solutions.append(solution)
        self.touch()

    def add_roadmap_phase(
        self,
        phase: RoadmapPhase,
    ) -> None:
        """
        Add roadmap phase.
        """
        self.roadmap_phases.append(phase)
        self.touch()

    def submit_for_review(self) -> None:
        """
        Submit recommendation for review.
        """
        if not self.solutions:
            raise ValueError(
                "Recommendation must contain at least one solution."
            )

        self.status = RecommendationStatus.UNDER_REVIEW
        self.submitted_at = datetime.now(UTC)
        self.touch()

    def approve(self) -> None:
        """
        Approve recommendation.
        """
        if self.status != RecommendationStatus.UNDER_REVIEW:
            raise ValueError(
                "Recommendation must be under review before approval."
            )

        self.status = RecommendationStatus.APPROVED
        self.approved_at = datetime.now(UTC)
        self.touch()

    def reject(self) -> None:
        """
        Reject recommendation.
        """
        self.status = RecommendationStatus.REJECTED
        self.touch()

    def archive(self) -> None:
        """
        Archive recommendation.
        """
        self.status = RecommendationStatus.ARCHIVED
        self.touch()