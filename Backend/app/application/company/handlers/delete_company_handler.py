"""
Delete Company application handler.
"""

from __future__ import annotations

from app.application.common.exceptions.not_found_exception import NotFoundException
from app.application.common.exceptions.validation_exception import ValidationException
from app.application.common.interfaces.unit_of_work import UnitOfWork
from app.application.company.company_commands import DeleteCompanyCommand
from app.domain.company.identifiers.company_id import CompanyId


class DeleteCompanyHandler:
    """Handles Delete Company use case."""

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: DeleteCompanyCommand) -> None:
        try:
            company_id = CompanyId(command.company_id)
        except (TypeError, ValueError) as exc:
            raise ValidationException(
                message="Invalid company id.",
                details={"company_id": command.company_id},
            ) from exc

        async with self._unit_of_work:
            repository = self._unit_of_work.company_repository
            company = await repository.get_by_id(company_id)

            if company is None:
                raise NotFoundException(
                    message="Company not found.",
                    details={"company_id": command.company_id},
                )

            await repository.delete(company_id)
            await self._unit_of_work.commit()
