"""
Lead Search Request

Defines the search criteria passed
to lead providers.
"""

from typing import Optional

from pydantic import BaseModel, Field


class LeadSearchRequest(BaseModel):
    """
    Search criteria.
    """

    company_name: Optional[str] = None

    website: Optional[str] = None

    industry: Optional[str] = None

    country: Optional[str] = None

    state: Optional[str] = None

    city: Optional[str] = None

    keywords: list[str] = Field(
        default_factory=list,
    )

    employee_min: Optional[int] = None

    employee_max: Optional[int] = None

    limit: int = Field(
        default=25,
        ge=1,
        le=1000,
    )