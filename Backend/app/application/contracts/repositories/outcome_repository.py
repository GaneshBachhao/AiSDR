"""
Outcome repository contract.

Defines the application-facing persistence contract for OutcomeEvent.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.outcome.entities.outcome_event import OutcomeEvent
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId


class OutcomeRepository(Repository[OutcomeEvent, OutcomeEventId]):
    """Repository contract for OutcomeEvent aggregates."""

    @abstractmethod
    async def list_by_lead(self, lead_id: LeadId) -> list[OutcomeEvent]:
        raise NotImplementedError

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[OutcomeEvent]:
        raise NotImplementedError
