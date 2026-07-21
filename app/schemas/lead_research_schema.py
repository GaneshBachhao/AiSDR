from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LeadResearchBase(BaseModel):
    company_name: str

    industry: Optional[str] = None

    summary: Optional[str] = None

    business_model: Optional[str] = None

    pain_points: Optional[str] = None

    ai_opportunities: Optional[str] = None

    recommended_services: Optional[str] = None

    decision_makers: Optional[str] = None

    buying_signals: Optional[str] = None

    confidence_score: Optional[float] = None

    matched_sector: str | None = None

    sector_confidence: float | None = None

    catalog_services: str | None = None

    generic_ai_opportunities: str | None = None

    catalog_version: str | None = None

    model_name: Optional[str] = None


class LeadResearchCreate(LeadResearchBase):
    lead_id: int


class LeadResearchResponse(LeadResearchBase):
    id: int

    lead_id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )