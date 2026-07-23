from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LeadResponse(BaseModel):
    """
    Lead response schema.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    company_name: str

    contact_name: str

    email: str

    phone: str | None

    website: str | None

    notes: str | None

    created_at: datetime