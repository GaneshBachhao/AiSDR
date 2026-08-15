"""
Qualification persistence mapper.

Maps the Qualification aggregate to and from the existing
``qualifications`` table without changing any other aggregate.
"""

from __future__ import annotations

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.qualification.entities.qualification import Qualification
from app.domain.qualification.enums.qualification_status import QualificationStatus
from app.domain.qualification.identifiers.qualification_id import QualificationId
from app.domain.qualification.value_objects.qualification_score import QualificationScore
from app.infrastructure.persistence.models.qualification_model import QualificationModel


class QualificationPersistenceMapper:
    """Map Qualification domain objects to and from ORM models."""

    @staticmethod
    def to_model(qualification: Qualification) -> QualificationModel:
        return QualificationModel(
            id=qualification.id.value,
            lead_id=qualification.lead_id.value,
            assessment_id=qualification.assessment_id.value,
            status=qualification.status.value,
            score=qualification.score.value,
            recommendation=qualification.recommendation,
            created_at=qualification.created_at,
            updated_at=qualification.updated_at,
        )

    @staticmethod
    def to_domain(model: QualificationModel) -> Qualification:
        """Rehydrate the aggregate preserving its persisted identity."""
        qualification = Qualification(
            lead_id=LeadId(model.lead_id),
            assessment_id=AssessmentId(model.assessment_id),
            qualification_id=QualificationId(model.id),
        )

        qualification._status = QualificationStatus(model.status)
        qualification._score = QualificationScore(
            0.0 if model.score is None else model.score,
        )
        qualification._recommendation = model.recommendation
        qualification._created_at = model.created_at
        qualification._updated_at = model.updated_at

        return qualification
