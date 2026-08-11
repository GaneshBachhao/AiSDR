"""
Qualification aggregate.
"""

from __future__ import annotations

from datetime import UTC
from datetime import datetime

from app.domain.qualification.enums.qualification_status import (
    QualificationStatus,
)
from app.domain.qualification.identifiers.qualification_id import (
    QualificationId,
)
from app.domain.qualification.value_objects.qualification_score import (
    QualificationScore,
)
from app.domain.shared.base.aggregate_root import (
    AggregateRoot,
)
from app.domain.lead.identifiers.lead_id import (
    LeadId,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)


class Qualification(
    AggregateRoot[
        QualificationId,
    ],
):
    """
    Qualification aggregate.
    """

    def __init__(
        self,
        lead_id: LeadId,
        assessment_id: AssessmentId,
        qualification_id: QualificationId | None = None,
    ) -> None:
        self.id = qualification_id or QualificationId.generate()

        self._lead_id = lead_id

        self._assessment_id = assessment_id

        self._status = (
            QualificationStatus.PARTIALLY_QUALIFIED
        )

        self._score = QualificationScore(
            0,
        )

        self._recommendation: str | None = None

        self._created_at = datetime.now(
            UTC,
        )

        self._updated_at = datetime.now(
            UTC,
        )

    @property
    def lead_id(
        self,
    ) -> LeadId:
        return self._lead_id

    @property
    def assessment_id(
        self,
    ) -> AssessmentId:
        return self._assessment_id

    @property
    def status(
        self,
    ) -> QualificationStatus:
        return self._status

    @property
    def score(
        self,
    ) -> QualificationScore:
        return self._score

    @property
    def recommendation(
        self,
    ) -> str | None:
        return self._recommendation

    @property
    def created_at(
        self,
    ) -> datetime:
        return self._created_at

    @property
    def updated_at(
        self,
    ) -> datetime:
        return self._updated_at

    def update_score(
        self,
        score: QualificationScore,
    ) -> None:
        """
        Update qualification score.
        """

        self._score = score

        self._updated_at = datetime.now(
            UTC,
        )

    def update_status(
        self,
        status: QualificationStatus,
    ) -> None:
        """
        Update qualification status.
        """

        self._status = status

        self._updated_at = datetime.now(
            UTC,
        )

    def update_recommendation(
        self,
        recommendation: str | None,
    ) -> None:
        """
        Update recommendation.
        """

        self._recommendation = recommendation

        self._updated_at = datetime.now(
            UTC,
        )