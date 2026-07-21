from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OutreachBase(BaseModel):
    """
    Base schema for AI-generated outreach.
    """

    channel: str

    subject: Optional[str] = None

    message: str

    call_to_action: Optional[str] = None

    status: str = "DRAFT"

    version: int = 1


class OutreachCreate(OutreachBase):
    """
    Schema used when creating outreach.
    """

    lead_id: int

    lead_research_id: int


class OutreachResponse(OutreachBase):
    """
    Schema returned from API/database.
    """

    id: int

    lead_id: int

    lead_research_id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )