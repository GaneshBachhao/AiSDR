"""Recommendation domain <-> ORM mapper."""

from __future__ import annotations

import json
from uuid import UUID

from app.domain.assessment.identifiers.assessment_id import AssessmentId
from app.domain.recommendation.entities.recommendation import Recommendation
from app.domain.recommendation.entities.solution import Solution
from app.domain.recommendation.enums.recommendation_status import RecommendationStatus
from app.domain.recommendation.identifiers.recommendation_id import RecommendationId
from app.infrastructure.persistence.models.recommendation_model import RecommendationModel


def _solution_to_dict(solution: Solution) -> dict:
    return {
        "solution_id": str(solution.solution_id),
        "title": solution.title,
        "description": solution.description,
        "solution_type": solution.solution_type.value,
        "priority": solution.priority.value,
        "is_existing_offering": solution.is_existing_offering,
    }


def _solution_from_dict(data: dict) -> Solution:
    return Solution(
        solution_id=UUID(data["solution_id"]),
        title=data["title"],
        description=data["description"],
        solution_type=data["solution_type"],
        priority=data["priority"],
        is_existing_offering=data.get("is_existing_offering", True),
    )


class RecommendationMapper:
    """Map Recommendation aggregates to and from the existing table.

    Note: only ``solutions`` (title/description/type/priority/
    is_existing_offering) round-trips through persistence today --
    ``status``/``roadmap_phases``/``submitted_at``/``approved_at`` have no
    backing columns in ``RecommendationModel`` and are not restored on
    ``to_domain`` (pre-existing gap, not introduced by this change; flagged
    in docs/product_backlog.md rather than expanded here).
    """

    @staticmethod
    def to_model(domain: Recommendation) -> RecommendationModel:
        return RecommendationModel(
            id=domain.id.value,
            assessment_id=domain.assessment_id.value,
            summary=domain.executive_summary or "",
            solutions=json.dumps([_solution_to_dict(s) for s in domain.solutions]),
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    @staticmethod
    def to_domain(model: RecommendationModel) -> Recommendation:
        solutions = [
            _solution_from_dict(item)
            for item in json.loads(model.solutions or "[]")
        ]
        recommendation = Recommendation(
            id=RecommendationId(model.id),
            assessment_id=AssessmentId(model.assessment_id),
            status=RecommendationStatus.DRAFT,
            executive_summary=model.summary,
            solutions=solutions,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return recommendation
