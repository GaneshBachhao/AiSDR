"""
Company Profile Schema

Represents the canonical company intelligence
object used throughout AgneticAI.

This profile is produced by the Company
Intelligence Engine and consumed by
qualification, research, recommendations,
proposal generation, and outreach.
"""

from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    """
    Canonical company intelligence model.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    company_name: str

    website: str | None = None

    linkedin_url: str | None = None

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    country: str | None = None

    state: str | None = None

    city: str | None = None

    # ---------------------------------------------------------
    # Business
    # ---------------------------------------------------------

    industry: str | None = None

    description: str | None = None

    employee_count: int | None = None

    estimated_revenue: str | None = None

    # ---------------------------------------------------------
    # Intelligence
    # ---------------------------------------------------------

    products: list[str] = Field(default_factory=list)

    services: list[str] = Field(default_factory=list)

    technologies: list[str] = Field(default_factory=list)

    certifications: list[str] = Field(default_factory=list)

    # ---------------------------------------------------------
    # AI Assessment
    # ---------------------------------------------------------

    ai_readiness: str | None = None

    confidence: float = Field(
        default=0.0,
        ge=0,
        le=1,
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    source: str = "gemini"

    metadata: dict = Field(
        default_factory=dict,
    )