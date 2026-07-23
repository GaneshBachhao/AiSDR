"""
Discover Companies Command

Represents a request to discover companies.
"""

from pydantic import BaseModel, ConfigDict, Field


class DiscoverCompaniesCommand(BaseModel):
    """
    Command used by the DiscoverCompaniesHandler.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    industry: str = Field(
        ...,
        min_length=1,
        description="Target industry",
    )

    location: str = Field(
        ...,
        min_length=1,
        description="Target location",
    )

    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum companies to discover",
    )