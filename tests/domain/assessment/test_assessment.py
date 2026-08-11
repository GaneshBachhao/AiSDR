from __future__ import annotations

from uuid import uuid4

import pytest

from app.domain.assessment.entities.assessment import Assessment
from app.domain.assessment.enums.assessment_status import AssessmentStatus
from app.domain.assessment.enums.maturity_level import MaturityLevel
from app.domain.assessment.services.assessment_service import AssessmentService
from app.domain.assessment.value_objects.assessment_score import AssessmentScore
from app.domain.discovery.identifiers.discovery_id import (
    DiscoveryId,
)


def test_assessment_start_and_complete_update_state() -> None:
    assessment = Assessment(
        discovery_id=DiscoveryId(uuid4()),
    )

    AssessmentService.start(assessment)

    assert assessment.status is AssessmentStatus.IN_PROGRESS
    assert assessment.started_at is not None

    AssessmentService.complete(assessment, summary="Assessment complete")

    assert assessment.status is AssessmentStatus.COMPLETED
    assert assessment.completed_at is not None
    assert assessment.summary == "Assessment complete"


@pytest.mark.parametrize(
    ("score", "expected_maturity"),
    [
        (AssessmentScore(overall_score=10), MaturityLevel.INITIAL),
        (AssessmentScore(overall_score=25), MaturityLevel.DEVELOPING),
        (AssessmentScore(overall_score=45), MaturityLevel.DEFINED),
        (AssessmentScore(overall_score=70), MaturityLevel.MANAGED),
        (AssessmentScore(overall_score=95), MaturityLevel.OPTIMIZED),
    ],
)
def test_assessment_service_determines_maturity_from_score(
    score: AssessmentScore,
    expected_maturity: MaturityLevel,
) -> None:
    assert AssessmentService.determine_maturity(score) is expected_maturity
