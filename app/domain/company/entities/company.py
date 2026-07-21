from __future__ import annotations

from dataclasses import dataclass

from app.domain.common.entities.base_entity import BaseEntity
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry


@dataclass
class Company(BaseEntity):
    """
    Aggregate root representing a client organization.

    A Company is the central business entity within the AI Consulting
    platform. It contains only stable business information. Operational
    information such as assessments, recommendations, workflows and
    opportunities belong to their respective domains.
    """

    name: str

    website: str | None = None

    industry: Industry | None = None

    company_size: CompanySize | None = None

    country: str | None = None

    state: str | None = None

    city: str | None = None

    is_active: bool = True

    def update_name(self, name: str) -> None:
        """Update company name."""

        self.name = name.strip()
        self.touch()

    def update_website(self, website: str | None) -> None:
        """Update company website."""

        self.website = website
        self.touch()

    def update_location(
        self,
        *,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
    ) -> None:
        """Update company headquarters."""

        if country is not None:
            self.country = country

        if state is not None:
            self.state = state

        if city is not None:
            self.city = city

        self.touch()

    def update_industry(self, industry: Industry) -> None:
        """Assign company industry."""

        self.industry = industry
        self.touch()

    def update_company_size(self, company_size: CompanySize) -> None:
        """Assign company size."""

        self.company_size = company_size
        self.touch()

    def activate(self) -> None:
        """Activate the company."""

        self.is_active = True
        self.touch()

    def deactivate(self) -> None:
        """Deactivate the company."""

        self.is_active = False
        self.touch()