"""List Suppressions application handler."""

from __future__ import annotations

from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.suppression.dto.suppression_responses import (
    SuppressionEntryResponseDTO,
)
from app.application.suppression.suppression_mapper import SuppressionMapper


class ListSuppressionsHandler:
    """List all suppression entries."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, skip: int = 0, limit: int = 100) -> list[SuppressionEntryResponseDTO]:
        async with self._unit_of_work:
            entries = await self._unit_of_work.suppression_repository.list(skip=skip, limit=limit)

        return SuppressionMapper.to_response_list(entries)
