"""
Sequence repository contract.

Defines the application-facing persistence contract for Sequence.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.identifiers.sequence_id import SequenceId


class SequenceRepository(Repository[Sequence, SequenceId]):
    """Repository contract for Sequence aggregates."""

    @abstractmethod
    async def list_by_lead(self, lead_id: LeadId) -> list[Sequence]:
        raise NotImplementedError
