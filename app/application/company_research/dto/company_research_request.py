from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class CompanyResearchRequest(BaseModel):
    """Input for automated public-web company discovery."""

    industries: list[str] = Field(default_factory=list)
    geography: str
    company_size: list[str] = Field(default_factory=list)
    revenue_range: str | None = None
    technologies: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    ideal_customer_profile: str | None = None
    number_of_companies: int = Field(default=10, ge=1, le=50)
    research_period: str = "last 6 months"
    minimum_qualification_score: int = Field(default=0, ge=0, le=100)
    preferred_decision_makers: list[str] = Field(default_factory=list)
    target_language: str = "English"

    @field_validator("industries", "company_size", "technologies", "services", "preferred_decision_makers")
    @classmethod
    def clean_lists(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item and item.strip()]
