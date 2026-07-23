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

from app.application.discovery.commands.discover_companies import (
    DiscoverCompaniesCommand,
)

from app.application.discovery.dto.discovery_response_dto import (
    DiscoveryResponseDTO,
)

from app.application.discovery.mappers.discovery_mapper import (
    DiscoveryMapper,
)

from app.application.discovery.validators.discover_companies_validator import (
    DiscoverCompaniesValidator,
)

from app.discovery.services.discovery_service import (
    DiscoveryService,
)


class DiscoverCompaniesHandler(
    BaseHandler[
        DiscoverCompaniesCommand,
        DiscoveryResponseDTO,
    ]
):
    """
    Application handler responsible for
    discovering companies.

    Responsibilities:

    - Validate request
    - Execute discovery service
    - Map results
    - Return HandlerResult

    No business logic belongs here.
    """

    def __init__(
        self,
        discovery_service: DiscoveryService,
        validator: DiscoverCompaniesValidator,
    ) -> None:

        super().__init__()

        self._discovery_service = discovery_service
        self._validator = validator

    async def handle(
        self,
        command: DiscoverCompaniesCommand,
        context: HandlerContext,
    ) -> HandlerResult[DiscoveryResponseDTO]:

        validation = self._validator.validate(
            command,
        )

        if not validation.is_valid:

            return HandlerResult.failure(
                message="Discovery request validation failed.",
                errors=validation.error_messages(),
            )

        request_dto = (
            DiscoveryMapper.command_to_dto(
                command,
            )
        )

        discovery_request = (
            DiscoveryMapper.dto_to_schema(
                request_dto,
            )
        )

        results = (
            self._discovery_service.discover(
                discovery_request,
            )
        )

        response = (
            DiscoveryMapper.results_to_response(
                results,
            )
        )

        return HandlerResult.ok(
            data=response,
            message="Companies discovered successfully.",
        )