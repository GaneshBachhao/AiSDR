"""
Suppression repository contract.

Defines the application-facing persistence contract for SuppressionEntry.
"""

from __future__ import annotations

from abc import abstractmethod

from app.application.common.interfaces.repository import Repository
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId


class SuppressionRepository(Repository[SuppressionEntry, SuppressionEntryId]):
    """Repository contract for SuppressionEntry aggregates."""

    @abstractmethod
    async def find_by_email(self, email: str) -> SuppressionEntry | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[SuppressionEntry]:
        raise NotImplementedError
