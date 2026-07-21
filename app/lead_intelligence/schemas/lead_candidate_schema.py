"""
Lead Candidate Schema

Represents a normalized lead returned
by any lead provider.

This object is NOT persisted directly.

It is transformed into a Lead during
Discovery.
"""

from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class LeadCandidate(BaseModel):
    """
    Normalized lead candidate.
    """

    company_name: str = Field(
        ...,
        description="Company name",
    )

    website: Optional[HttpUrl] = Field(
        default=None,
        description="Company website",
    )

    industry: Optional[str] = None

    country: Optional[str] = None

    state: Optional[str] = None

    city: Optional[str] = None

    linkedin_url: Optional[HttpUrl] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    employee_count: Optional[int] = None

    source: str = Field(
        ...,
        description="Lead source",
    )

    confidence: float = Field(
        default=1.0,
        ge=0,
        le=1,
    )

    metadata: dict = Field(
        default_factory=dict,
        description="Provider specific metadata",
    )