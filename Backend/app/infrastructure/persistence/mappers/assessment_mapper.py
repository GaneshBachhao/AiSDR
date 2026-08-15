"""
Assessment persistence mapper.

Maps the Assessment aggregate to the existing assessments table without
changing Company, Contact, Lead or Discovery persistence contracts.
"""
from __future__ import annotations

from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.enums.assessment_status import AssessmentStatus
from app.domain.assessment.enums.maturity_level import MaturityLevel
from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.assessment.value_objects.assessment_score import AssessmentScore
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.infrastructure.persistence.models.assessment_model import AssessmentModel


class AssessmentMapper:
    """Maps Assessment domain objects to persistence models and back."""

    @staticmethod
    def to_model(assessment: Assessment) -> AssessmentModel:
        return AssessmentModel(
            id=assessment.id.value,
            discovery_id=assessment.discovery_id.value,
            status=assessment.status.value,
            started_at=assessment.started_at,
            completed_at=assessment.completed_at,
            summary=assessment.summary,
            maturity_level=assessment.maturity_level.value,
            readiness_score=assessment.score.overall_score,
            strengths=assessment.strengths,
            weaknesses=assessment.weaknesses,
            opportunities=assessment.opportunities_summary,
            risks=assessment.risks,
        )

    @staticmethod
    def to_domain(model: AssessmentModel) -> Assessment:
        try:
            status = AssessmentStatus(model.status)
        except ValueError:
            status = AssessmentStatus[str(model.status).strip().upper().replace(" ", "_")]

        try:
            maturity = (
                MaturityLevel(model.maturity_level)
                if model.maturity_level
                else MaturityLevel.INITIAL
            )
        except ValueError:
            maturity = MaturityLevel[
                str(model.maturity_level).strip().upper().replace(" ", "_")
            ]

        return Assessment(
            id=AssessmentId(model.id),
            discovery_id=DiscoveryId(model.discovery_id),
            status=status,
            started_at=model.started_at,
            completed_at=model.completed_at,
            summary=model.summary,
            maturity_level=maturity,
            score=AssessmentScore(
                overall_score=(
                    0.0
                    if model.readiness_score is None
                    else model.readiness_score
                ),
            ),
            strengths=model.strengths,
            weaknesses=model.weaknesses,
            opportunities_summary=model.opportunities,
            risks=model.risks,
        )

    @staticmethod
    def update_model(
        model: AssessmentModel,
        assessment: Assessment,
    ) -> AssessmentModel:
        model.status = assessment.status.value
        model.started_at = assessment.started_at
        model.completed_at = assessment.completed_at
        model.summary = assessment.summary
        model.maturity_level = assessment.maturity_level.value
        model.readiness_score = assessment.score.overall_score
        model.strengths = assessment.strengths
        model.weaknesses = assessment.weaknesses
        model.opportunities = assessment.opportunities_summary
        model.risks = assessment.risks
        return model
