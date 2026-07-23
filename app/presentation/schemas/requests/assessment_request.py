from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateAssessmentRequest(BaseModel):
    """
    Create assessment request.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    discovery_id: UUID