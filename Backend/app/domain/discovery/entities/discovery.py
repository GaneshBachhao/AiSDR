"""
Discovery aggregate root.

Architecture Freeze v5.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.discovery.enums.discovery_status import DiscoveryStatus
from app.domain.discovery.identifiers.discovery_id import DiscoveryId
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class Discovery(AggregateRoot[DiscoveryId]):
    """
    Aggregate root representing discovery information collected for a lead.

    Business invariants:
    - A lead id is mandatory.
    - Discovery text is normalized at the aggregate boundary.
    - Lifecycle changes update the aggregate timestamp.
    """

    lead_id: LeadId = field(kw_only=True)
    id: DiscoveryId = field(default_factory=DiscoveryId, kw_only=True)

    problem_statement: str | None = None
    current_solution: str | None = None
    business_impact: str | None = None
    success_criteria: str | None = None

    status: DiscoveryStatus = DiscoveryStatus.CREATED

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __post_init__(self) -> None:
        """Validate and normalize discovery data."""
        self._validate()
        self.problem_statement = self._normalize(self.problem_statement)
        self.current_solution = self._normalize(self.current_solution)
        self.business_impact = self._normalize(self.business_impact)
        self.success_criteria = self._normalize(self.success_criteria)

    def _validate(self) -> None:
        if self.lead_id is None:
            raise ValueError("Lead ID cannot be empty.")

    @staticmethod
    def _normalize(value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    # ---------------------------------------------------------
    # Lifecycle operations
    # ---------------------------------------------------------

    def start(self) -> None:
        """Move the discovery into progress."""
        self.status = DiscoveryStatus.IN_PROGRESS
        self.touch()

    def hold(self) -> None:
        """Put the discovery on hold."""
        self.status = DiscoveryStatus.ON_HOLD
        self.touch()

    def complete(self) -> None:
        """Mark the discovery as completed."""
        self.status = DiscoveryStatus.COMPLETED
        self.touch()

    def cancel(self) -> None:
        """Cancel the discovery."""
        self.status = DiscoveryStatus.CANCELLED
        self.touch()

    def update_status(self, status: DiscoveryStatus) -> None:
        """Set the lifecycle status using the domain enum."""
        if not isinstance(status, DiscoveryStatus):
            raise ValueError("Invalid discovery status.")
        self.status = status
        self.touch()

    # ---------------------------------------------------------
    # Detail operations
    # ---------------------------------------------------------

    def update_details(
        self,
        *,
        problem_statement: str | None = None,
        current_solution: str | None = None,
        business_impact: str | None = None,
        success_criteria: str | None = None,
    ) -> None:
        """
        Update supplied discovery details.

        None means "do not change" for update operations.
        """
        changed = False

        if problem_statement is not None:
            self.problem_statement = self._normalize(problem_statement)
            changed = True

        if current_solution is not None:
            self.current_solution = self._normalize(current_solution)
            changed = True

        if business_impact is not None:
            self.business_impact = self._normalize(business_impact)
            changed = True

        if success_criteria is not None:
            self.success_criteria = self._normalize(success_criteria)
            changed = True

        if changed:
            self.touch()
