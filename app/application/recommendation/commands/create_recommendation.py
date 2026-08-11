from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateRecommendationCommand(BaseModel):
    """
    Command to create a recommendation
    from an assessment.
    """

    model_config = ConfigDict(
        frozen=True
    )

    assessment_id: UUID