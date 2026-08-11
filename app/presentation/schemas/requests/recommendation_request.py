from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GenerateRecommendationRequest(BaseModel):
    """
    Generate recommendation request.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    assessment_id: UUID