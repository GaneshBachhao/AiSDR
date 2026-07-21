from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from app.leads.enums.lead_status import (
    LeadStatus,
)

class LeadBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    status: LeadStatus | None = None
    notes: Optional[str] = None


class LeadResponse(LeadBase):
    id: int
    status: LeadStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)