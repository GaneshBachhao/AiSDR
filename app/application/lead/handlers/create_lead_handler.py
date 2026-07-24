from app.application.contracts.repositories.lead_repository import (
    LeadRepository,
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
        repository: LeadRepository,
        validator: CreateLeadValidator,
        mapper: LeadMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper


    async def handle(
        self,
        command: CreateLeadCommand,
    ) -> LeadDTO:

        validation = self._validator.validate(command)

        if not validation.is_valid:
            raise ValueError(validation.errors)

        lead = self._mapper.to_domain(command)

        await self._repository.add(lead)

        return self._mapper.to_dto(lead)