from __future__ import annotations

from dataclasses import dataclass

from app.domain.company.value_objects.company_size import (
    CompanySize,
)
from app.domain.company.value_objects.industry import (
    Industry,
)


@dataclass(frozen=True)
class CompanyProfile:
    """
    Immutable company business profile information.
    """

    industry: Industry

    company_size: CompanySize

    country: str | None = None

    state: str | None = None

    city: str | None = None
