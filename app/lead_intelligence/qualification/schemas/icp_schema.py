"""
Ideal Customer Profile (ICP)

Defines the characteristics of companies
that AgneticAI should target during lead
discovery and qualification.
"""

from pydantic import BaseModel, Field


class IdealCustomerProfile(BaseModel):
    """
    Defines the desired characteristics of
    a target company.
    """

    industries: list[str] = Field(
        default_factory=list,
        description="Target industries",
    )

    locations: list[str] = Field(
        default_factory=list,
        description="Preferred cities, states or countries",
    )

    employee_min: int | None = Field(
        default=None,
        ge=1,
    )

    employee_max: int | None = Field(
        default=None,
        ge=1,
    )

    exclude_industries: list[str] = Field(
        default_factory=list,
    )

    include_keywords: list[str] = Field(
        default_factory=list,
    )

    exclude_keywords: list[str] = Field(
        default_factory=list,
    )

    require_official_website: bool = True

    minimum_confidence: float = Field(
        default=0.70,
        ge=0.0,
        le=1.0,
    )

    passing_score: float = Field(
        default=70,
        ge=0,
        le=100,
        description="Minimum score required to qualify a lead",
    )