from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AssessmentResponse(BaseModel):
    """
    Assessment response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    discovery_id: UUID
    maturity_score: int
    status: str
    created_at: datetime