"""
Enrich Company Response DTO

Returned by the EnrichCompanyHandler.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class EnrichCompanyResponseDTO(BaseModel):
    """
    Response DTO containing the enriched company profile.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    company_name: str

    website: str | None = None

    linkedin_url: str | None = None

    country: str | None = None

    state: str | None = None

    city: str | None = None

    industry: str | None = None

    description: str | None = None

    employee_count: int | None = None

    estimated_revenue: float | None = None

    products: list[str] = Field(
        default_factory=list,
    )

    services: list[str] = Field(
        default_factory=list,
    )

    technologies: list[str] = Field(
        default_factory=list,
    )

    certifications: list[str] = Field(
        default_factory=list,
    )

    ai_readiness: str | None = None

    confidence: float

    source: str

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )