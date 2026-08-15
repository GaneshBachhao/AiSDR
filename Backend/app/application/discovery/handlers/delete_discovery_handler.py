"""Delete Discovery application handler."""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.discovery.discovery_commands import DeleteDiscoveryCommand
from app.application.discovery.discovery_validator import DiscoveryValidator
from app.domain.discovery.identifiers.discovery_id import DiscoveryId


class DeleteDiscoveryHandler:
    """Handle the Delete Discovery use case."""

    def __init__(self, unit_of_work: UnitOfWork, validator: DiscoveryValidator) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator

    async def handle(self, command: DeleteDiscoveryCommand) -> None:
        validation = self._validator.validate_delete(command)
        if not validation.is_valid:
            raise ValidationException(
                message="Discovery validation failed.",
                details={error.field: error.message for error in validation.errors},
            )

        try:
            discovery_id = DiscoveryId(command.discovery_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Discovery validation failed.",
                details={"discovery_id": str(exc)},
            ) from exc

        async with self._unit_of_work:
            discovery = await self._unit_of_work.discovery_repository.get_by_id(discovery_id)
            if discovery is None:
                raise NotFoundException(
                    message="Discovery session not found.",
                    details={"discovery_id": command.discovery_id},
                )

            await self._unit_of_work.discovery_repository.delete(discovery_id)
            await self._unit_of_work.commit()
