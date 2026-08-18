from __future__ import annotations

import pytest

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.enums.recommendation_status import RecommendationStatus


def _solution(**overrides) -> Solution:
    defaults = dict(
        title="Automate reporting",
        description="Automate the monthly reporting workflow.",
        solution_type="Automation",
        priority="High",
        is_existing_offering=True,
    )
    defaults.update(overrides)
    return Solution(**defaults)


def test_defaults_to_draft() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())

    assert recommendation.status is RecommendationStatus.DRAFT
    assert recommendation.submitted_at is None
    assert recommendation.approved_at is None
    assert recommendation.solutions == []


def test_add_solution_appends_and_touches() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())
    updated_before = recommendation.updated_at

    recommendation.add_solution(_solution())

    assert len(recommendation.solutions) == 1
    assert recommendation.updated_at >= updated_before


def test_submit_for_review_requires_at_least_one_solution() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())

    with pytest.raises(ValueError):
        recommendation.submit_for_review()

    assert recommendation.status is RecommendationStatus.DRAFT


def test_submit_for_review_moves_to_under_review_and_sets_submitted_at() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())
    recommendation.add_solution(_solution())

    recommendation.submit_for_review()

    assert recommendation.status is RecommendationStatus.UNDER_REVIEW
    assert recommendation.submitted_at is not None


def test_submit_is_an_alias_for_submit_for_review() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())
    recommendation.add_solution(_solution())

    recommendation.submit()

    assert recommendation.status is RecommendationStatus.UNDER_REVIEW


def test_approve_requires_under_review_status() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())

    with pytest.raises(ValueError):
        recommendation.approve()

    assert recommendation.status is RecommendationStatus.DRAFT


def test_approve_moves_to_approved_and_sets_approved_at() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())
    recommendation.add_solution(_solution())
    recommendation.submit_for_review()

    recommendation.approve()

    assert recommendation.status is RecommendationStatus.APPROVED
    assert recommendation.approved_at is not None


def test_approve_cannot_be_called_twice() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())
    recommendation.add_solution(_solution())
    recommendation.submit_for_review()
    recommendation.approve()

    with pytest.raises(ValueError):
        recommendation.approve()


def test_reject_sets_status_regardless_of_current_state() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())

    recommendation.reject()

    assert recommendation.status is RecommendationStatus.REJECTED


def test_archive_sets_status() -> None:
    recommendation = Recommendation(assessment_id=AssessmentId())

    recommendation.archive()

    assert recommendation.status is RecommendationStatus.ARCHIVED


def test_add_roadmap_phase_appends_and_touches() -> None:
    from app.domain.recommendation.entities.roadmap_phase import RoadmapPhase

    recommendation = Recommendation(assessment_id=AssessmentId())
    updated_before = recommendation.updated_at

    recommendation.add_roadmap_phase(
        RoadmapPhase(
            phase_name="Phase 1",
            sequence=1,
            description="Discovery",
            estimated_duration="2 weeks",
        )
    )

    assert len(recommendation.roadmap_phases) == 1
    assert recommendation.updated_at >= updated_before
