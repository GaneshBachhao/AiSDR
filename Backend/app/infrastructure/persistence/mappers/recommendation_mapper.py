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

    Note: ``roadmap_phases`` still has no backing column and is not
    restored on ``to_domain`` -- no application flow populates it yet
    (no handler ever calls ``add_roadmap_phase``), so it's left as a
    known, smaller remaining gap rather than expanded here.
    ``status``/``submitted_at``/``approved_at`` used to have the same gap
    (silently defaulting every loaded Recommendation back to Draft
    regardless of its real persisted status) -- fixed alongside wiring up
    Submit/Approve, since the RecommendationStatus.DRAFT hardcoding here
    is exactly why Submit/Approve appeared to work in a single request
    but never actually stuck.
    """

    @staticmethod
    def to_model(domain: Recommendation) -> RecommendationModel:
        return RecommendationModel(
            id=domain.id.value,
            assessment_id=domain.assessment_id.value,
            summary=domain.executive_summary or "",
            solutions=json.dumps([_solution_to_dict(s) for s in domain.solutions]),
            status=domain.status.value,
            submitted_at=domain.submitted_at,
            approved_at=domain.approved_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    @staticmethod
    def update_model(
        model: RecommendationModel,
        domain: Recommendation,
    ) -> RecommendationModel:
        """
        Update the already-persisted ORM row in place.

        This avoids merging a newly-constructed ORM instance that doesn't
        set the BaseModel audit-mixin columns (created_by/updated_by/
        is_deleted/deleted_at), the same defensive pattern
        CompanyMapper/AssessmentMapper/UserMapper already use.
        """
        model.summary = domain.executive_summary or ""
        model.solutions = json.dumps([_solution_to_dict(s) for s in domain.solutions])
        model.status = domain.status.value
        model.submitted_at = domain.submitted_at
        model.approved_at = domain.approved_at
        return model

    @staticmethod
    def to_domain(model: RecommendationModel) -> Recommendation:
        solutions = [_solution_from_dict(item) for item in json.loads(model.solutions or "[]")]
        recommendation = Recommendation(
            id=RecommendationId(model.id),
            assessment_id=AssessmentId(model.assessment_id),
            status=RecommendationStatus(model.status),
            executive_summary=model.summary,
            solutions=solutions,
            submitted_at=model.submitted_at,
            approved_at=model.approved_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return recommendation
