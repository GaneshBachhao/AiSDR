"""Delete OutcomeEvent application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.outcome.outcome_commands import DeleteOutcomeEventCommand
from app.domain.outcome.identifiers.outcome_event_id import OutcomeEventId


class DeleteOutcomeEventHandler:
    """Remove a mis-logged outcome."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: DeleteOutcomeEventCommand) -> None:
        outcome_id = OutcomeEventId(command.outcome_id)

        async with self._unit_of_work:
            exists = await self._unit_of_work.outcome_repository.exists(outcome_id)

            if not exists:
                raise NotFoundException(
                    message="Outcome event not found.",
                    details={"outcome_id": command.outcome_id},
                )

            await self._unit_of_work.outcome_repository.delete(outcome_id)
            await self._unit_of_work.commit()
