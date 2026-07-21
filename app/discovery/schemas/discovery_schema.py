from pydantic import BaseModel, Field


class DiscoveryRequest(BaseModel):
    """
    Request model for lead discovery.
    """

    industry: str = Field(
        ...,
        description="Target industry"
    )

    location: str = Field(
        ...,
        description="Target location"
    )

    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of companies to discover"
    )


class DiscoveryResult(BaseModel):
    """
    Represents a discovered company before it becomes a Lead.
    """

    company_name: str

    website: str | None = None

    industry: str | None = None

    location: str | None = None

    source: str

    description: str | None = None

    employee_range: str | None = None

    linkedin_url: str | None = None