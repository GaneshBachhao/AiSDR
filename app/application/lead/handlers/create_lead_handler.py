from __future__ import annotations

from app.application.common.handler.base_handler import (
    BaseHandler,
)

from app.application.common.handler.handler_context import (
    HandlerContext,
)

from app.application.common.handler.handler_result import (
    HandlerResult,
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

from app.domain.lead.entities.lead import (
    Lead,
)

from app.domain.lead.repositories.lead_repository import (
    LeadRepository,
)


class CreateLeadHandler(
    BaseHandler[
        CreateLeadCommand,
        LeadDTO,
    ]
):
    """
    Handles lead creation use case.
    """

    def __init__(
        self,
        repository: LeadRepository,
        validator,
        mapper: LeadMapper,
    ):
        self._repository = repository
        self._validator = validator
        self._mapper = mapper


    async def handle(
        self,
        request: CreateLeadCommand,
        context: HandlerContext,
    ) -> HandlerResult[LeadDTO]:

        # Validate request
        validation_result = (
            self._validator.validate(request)
        )

        if not validation_result.is_valid:
            return HandlerResult.failure(
                message="Lead validation failed",
                error_code="LEAD_VALIDATION_ERROR",
                errors=validation_result.errors,
                metadata=context.to_dict(),
            )


        # Create domain aggregate
        lead = Lead(
            company_name=request.company_name,
            contact_name=request.contact_name,
            email=request.email,
            phone=request.phone,
            website=request.website,
        )


        # Persist aggregate
        saved_lead = await self._repository.save(
            lead
        )


        # Convert to DTO
        response = self._mapper.to_dto(
            saved_lead
        )


        return HandlerResult.ok(
            data=response,
            message="Lead created successfully",
            metadata=context.to_dict(),
        )