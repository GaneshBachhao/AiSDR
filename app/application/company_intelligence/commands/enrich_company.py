"""
Enrich Company Command

Represents a request to enrich a discovered company.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import HttpUrl


class EnrichCompanyCommand(BaseModel):
    """
    Command consumed by EnrichCompanyHandler.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    company_name: str

    website: HttpUrl | None = None

    industry: str | None = None

    country: str | None = None

    state: str | None = None

    city: str | None = None

    linkedin_url: HttpUrl | None = None

    phone: str | None = None

    email: str | None = None

    employee_count: int | None = None

    source: str

    confidence: float = 1.0

    metadata: dict[str, object] = {}