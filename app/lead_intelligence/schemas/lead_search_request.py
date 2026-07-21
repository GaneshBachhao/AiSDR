from typing import Optional

from pydantic import BaseModel, Field


class LeadSearchRequest(BaseModel):
    """
    Search criteria for discovering companies.
    """

    industry: str = Field(
        ...,
        description="Target industry",
    )

    location: str = Field(
        ...,
        description="Target city/state/country",
    )

    keywords: list[str] = Field(
        default_factory=list,
        description="Additional search keywords",
    )

    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
    )