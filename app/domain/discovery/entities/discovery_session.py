from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.discovery.entities.discovery_response import DiscoveryResponse
from app.domain.discovery.enums.discovery_status import DiscoveryStatus
from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)
from app.domain.discovery.value_objects.business_goal import BusinessGoal
from app.domain.discovery.value_objects.pain_point import PainPoint
from app.domain.discovery.value_objects.stakeholder import Stakeholder
from app.domain.discovery.value_objects.technology import Technology
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class DiscoverySession(AggregateRoot[DiscoverySessionId]):
    """
    Aggregate root representing an AI discovery engagement.
    """

    id: DiscoverySessionId = field(
        default_factory=DiscoverySessionId,
        kw_only=True,
    )

    lead_id: LeadId

    company_id: str | None = None

    status: DiscoveryStatus = DiscoveryStatus.CREATED

    started_at: datetime | None = None

    completed_at: datetime | None = None

    summary: str | None = None

    notes: str | None = None

    responses: list[DiscoveryResponse] = field(
        default_factory=list,
    )

    pain_points: list[PainPoint] = field(
        default_factory=list,
    )

    business_goals: list[BusinessGoal] = field(
        default_factory=list,
    )

    technologies: list[Technology] = field(
        default_factory=list,
    )

    stakeholders: list[Stakeholder] = field(
        default_factory=list,
    )

    def start(self) -> None:
        """
        Start discovery.
        """
        self.status = DiscoveryStatus.IN_PROGRESS
        self.started_at = datetime.now(UTC)
        self.touch()

    def complete(
        self,
        summary: str | None = None,
    ) -> None:
        """
        Complete discovery.
        """
        self.status = DiscoveryStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.summary = summary
        self.touch()

    def add_response(
        self,
        response: DiscoveryResponse,
    ) -> None:
        self.responses.append(response)
        self.touch()

    def add_pain_point(
        self,
        pain_point: PainPoint,
    ) -> None:
        self.pain_points.append(pain_point)
        self.touch()

    def add_business_goal(
        self,
        goal: BusinessGoal,
    ) -> None:
        self.business_goals.append(goal)
        self.touch()

    def add_technology(
        self,
        technology: Technology,
    ) -> None:
        self.technologies.append(technology)
        self.touch()

    def add_stakeholder(
        self,
        stakeholder: Stakeholder,
    ) -> None:
        self.stakeholders.append(stakeholder)
        self.touch()

    def add_note(
        self,
        note: str,
    ) -> None:
        if self.notes:
            self.notes += f"\n{note}"
        else:
            self.notes = note

        self.touch()