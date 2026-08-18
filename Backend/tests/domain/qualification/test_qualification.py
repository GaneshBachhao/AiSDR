from __future__ import annotations

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.qualification.entities.qualification import Qualification
from app.domain.qualification.enums.qualification_status import QualificationStatus
from app.domain.qualification.value_objects.qualification_score import QualificationScore


def _qualification() -> Qualification:
    return Qualification(lead_id=LeadId(), assessment_id=AssessmentId())


def test_defaults_to_partially_qualified_with_zero_score() -> None:
    # Regression guard for the real, live-verified default: a new
    # Qualification always starts here regardless of what a caller
    # requests, unless explicitly overridden afterward (see
    # CreateQualificationHandler).
    qualification = _qualification()

    assert qualification.status is QualificationStatus.PARTIALLY_QUALIFIED
    assert qualification.score.value == 0
    assert qualification.recommendation is None


def test_update_status() -> None:
    qualification = _qualification()

    qualification.update_status(QualificationStatus.QUALIFIED)

    assert qualification.status is QualificationStatus.QUALIFIED


def test_update_score() -> None:
    qualification = _qualification()

    qualification.update_score(QualificationScore(88))

    assert qualification.score.value == 88


def test_update_recommendation() -> None:
    qualification = _qualification()

    qualification.update_recommendation("Strong fit, proceed to outreach.")

    assert qualification.recommendation == "Strong fit, proceed to outreach."


def test_update_recommendation_accepts_none() -> None:
    qualification = _qualification()
    qualification.update_recommendation("something")

    qualification.update_recommendation(None)

    assert qualification.recommendation is None


def test_updates_touch_updated_at() -> None:
    qualification = _qualification()
    updated_before = qualification.updated_at

    qualification.update_status(QualificationStatus.NEEDS_NURTURING)

    assert qualification.updated_at >= updated_before


def test_lead_and_assessment_ids_are_the_ones_passed_in() -> None:
    lead_id = LeadId()
    assessment_id = AssessmentId()

    qualification = Qualification(lead_id=lead_id, assessment_id=assessment_id)

    assert qualification.lead_id == lead_id
    assert qualification.assessment_id == assessment_id
