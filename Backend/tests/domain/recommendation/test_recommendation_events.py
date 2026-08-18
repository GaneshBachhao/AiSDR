"""
Tests for the Recommendation domain events.

Regression guard: recommendation_created.py and
recommendation_submitted_for_review.py both imported RecommendationId
from `..value_objects.recommendation_id`, a module that doesn't exist --
the real location is `..identifiers.recommendation_id`. This made the
whole `app.domain.recommendation.events` package fail to import (a
ModuleNotFoundError), found while writing these tests.
"""

from __future__ import annotations

from app.domain.recommendation.events.recommendation_approved import RecommendationApproved
from app.domain.recommendation.events.recommendation_created import RecommendationCreated
from app.domain.recommendation.events.recommendation_submitted_for_review import (
    RecommendationSubmittedForReview,
)
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId


def test_recommendation_created_carries_the_id_and_a_real_event_id():
    recommendation_id = RecommendationId()

    event = RecommendationCreated(recommendation_id=recommendation_id)

    assert event.recommendation_id == recommendation_id
    assert event.event_id is not None
    assert event.occurred_at is not None


def test_recommendation_submitted_for_review_carries_the_id():
    recommendation_id = RecommendationId()

    event = RecommendationSubmittedForReview(recommendation_id=recommendation_id)

    assert event.recommendation_id == recommendation_id
    assert event.event_id is not None


def test_recommendation_approved_carries_the_id():
    recommendation_id = RecommendationId()

    event = RecommendationApproved(recommendation_id=recommendation_id)

    assert event.recommendation_id == recommendation_id
    assert event.event_id is not None
