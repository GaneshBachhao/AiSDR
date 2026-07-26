"""
Create Lead application handler.
"""

from __future__ import annotations

from app.application.common.exceptions.validation_exception import (
    ValidationException,
)
from app.application.common.interfaces.unit_of_work import (
    UnitOfWork,
)
from app.application.lead.commands.create_lead import (
    CreateLeadCommand,
)
from app.application.lead.dto.lead_dto import (
    LeadDTO,
)
from app.application.lead.mappers.lead_mapper import (
    LeadMapper,
)
from app.application.lead.validators.create_lead_validator import (
    CreateLeadValidator,
)


class CreateLeadHandler:
    """
    Handles Create Lead use case.
    """

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        validator: CreateLeadValidator,
        mapper: LeadMapper,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._validator = validator
        self._mapper = mapper

    async def handle(
        self,
        command: CreateLeadCommand,
    ) -> LeadDTO:
        """
        Execute create lead workflow.
        """

        validation = self._validator.validate(command)

        if not validation.is_valid:
            raise ValidationException(
                message="Lead validation failed.",
                details={
                    error.field: error.message
                    for error in validation.errors
                },
            )

        lead = self._mapper.to_domain(command)

        async with self._unit_of_work:
            await self._unit_of_work.leads.add(lead)

        return self._mapper.to_dto(lead)