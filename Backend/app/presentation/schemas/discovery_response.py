from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class DiscoveryResponse(BaseModel):
    """
    Discovery response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    company_name: str
    website: HttpUrl
    status: str
    created_at: datetime
