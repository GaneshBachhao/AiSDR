"""
Discovery Response DTO

Returned by the Discovery Application Handler.
"""

from pydantic import BaseModel, ConfigDict


class DiscoveryCompanyDTO(BaseModel):
    """
    Represents a discovered company.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    company_name: str

    website: str | None = None

    industry: str | None = None

    location: str | None = None

    source: str

    description: str | None = None

    employee_range: str | None = None

    linkedin_url: str | None = None


class DiscoveryResponseDTO(BaseModel):
    """
    Collection of discovered companies.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    companies: list[DiscoveryCompanyDTO]