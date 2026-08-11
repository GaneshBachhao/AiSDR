from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.company.identifiers.company_id import CompanyId
from app.domain.company.value_objects.company_size import CompanySize
from app.domain.company.value_objects.industry import Industry
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Company(AggregateRoot[CompanyId]):
    """
    Aggregate root representing a client organization.

    Company size and employee count are intentionally separate:
    - employee_count is the known/estimated numeric headcount;
    - company_size is the business classification.
    """

    id: CompanyId = field(
        default_factory=CompanyId,
        kw_only=True,
    )

    name: str
    website: str | None = None
    industry: Industry | None = None
    company_size: CompanySize | None = None
    employee_count: int | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    is_active: bool = True

    def __post_init__(self) -> None:
        self._validate_name()
        self._validate_employee_count()

        self.name = self.name.strip()

        if self.website:
            self.website = self.website.strip()

        if self.country:
            self.country = self.country.strip()

        if self.state:
            self.state = self.state.strip()

        if self.city:
            self.city = self.city.strip()

    def _validate_name(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Company name cannot be empty.")

    def _validate_employee_count(self) -> None:
        if (
            self.employee_count is not None
            and self.employee_count < 0
        ):
            raise ValueError(
                "Employee count cannot be negative."
            )

    def update_name(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Company name cannot be empty.")
        self.name = name.strip()
        self.touch()

    def rename(self, name: str) -> None:
        """Backward-compatible alias for :meth:`update_name`."""
        self.update_name(name)

    def update_website(self, website: str | None) -> None:
        self.website = website.strip() if website else None
        self.touch()

    def update_industry(self, industry: Industry | None) -> None:
        self.industry = industry
        self.touch()

    def update_company_size(
        self,
        company_size: CompanySize | None,
    ) -> None:
        self.company_size = company_size
        self.touch()

    def update_employee_count(
        self,
        employee_count: int | None,
    ) -> None:
        if employee_count is not None and employee_count < 0:
            raise ValueError(
                "Employee count cannot be negative."
            )
        self.employee_count = employee_count
        self.touch()

    def update_location(
        self,
        *,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
    ) -> None:
        if country is not None:
            self.country = country.strip()
        if state is not None:
            self.state = state.strip()
        if city is not None:
            self.city = city.strip()
        self.touch()

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()
