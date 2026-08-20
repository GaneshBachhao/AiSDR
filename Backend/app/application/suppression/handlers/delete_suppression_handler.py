"""Delete Suppression application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.suppression.suppression_commands import DeleteSuppressionCommand
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId


class DeleteSuppressionHandler:
    """Lift a suppression."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: DeleteSuppressionCommand) -> None:
        suppression_id = SuppressionEntryId(command.suppression_id)

        async with self._unit_of_work:
            exists = await self._unit_of_work.suppression_repository.exists(suppression_id)

            if not exists:
                raise NotFoundException(
                    message="Suppression entry not found.",
                    details={"suppression_id": command.suppression_id},
                )

            await self._unit_of_work.suppression_repository.delete(suppression_id)
            await self._unit_of_work.commit()
