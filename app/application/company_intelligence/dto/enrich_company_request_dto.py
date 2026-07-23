"""
Enrich Company Request DTO

Internal request DTO used by the Application layer.
"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import HttpUrl


class EnrichCompanyRequestDTO(BaseModel):
    """
    Internal DTO for company enrichment.
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

    confidence: float

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )