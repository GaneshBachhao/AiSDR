"""
Discovery domain entity.

Represents a discovery session performed for a lead.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID, uuid4


@dataclass
class Discovery:
    """
    Domain entity representing discovery information
    collected during sales qualification.
    """

    lead_id: UUID

    id: UUID = field(default_factory=uuid4)

    problem_statement: str | None = None
    current_solution: str | None = None
    business_impact: str | None = None
    success_criteria: str | None = None

    completed: bool = False

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def complete(self) -> None:
        """
        Mark discovery as completed.
        """

        self.completed = True
        self.updated_at = datetime.now(UTC)

    def update_details(
        self,
        *,
        problem_statement: str | None = None,
        current_solution: str | None = None,
        business_impact: str | None = None,
        success_criteria: str | None = None,
    ) -> None:
        """
        Update discovery information.
        """

        if problem_statement is not None:
            self.problem_statement = problem_statement

        if current_solution is not None:
            self.current_solution = current_solution

        if business_impact is not None:
            self.business_impact = business_impact

        if success_criteria is not None:
            self.success_criteria = success_criteria

        self.updated_at = datetime.now(UTC)