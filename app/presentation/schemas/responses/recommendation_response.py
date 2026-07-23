from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationResponse(BaseModel):
    """
    Recommendation response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    assessment_id: UUID
    summary: str
    created_at: datetime