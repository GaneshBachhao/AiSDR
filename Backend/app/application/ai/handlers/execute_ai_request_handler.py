"""
Execute AI Request Handler
"""

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)
from app.application.ai.dto.ai_response_dto import (
    AIResponseDTO,
)
from app.application.ai.mappers.ai_mapper import (
    AIMapper,
)
from app.application.ai.validators.execute_ai_request_validator import (
    ExecuteAIRequestValidator,
)
from app.application.common.handler.base_handler import (
    BaseHandler,
)
from app.application.common.handler.handler_context import (
    HandlerContext,
)
from app.application.common.handler.handler_result import (
    HandlerResult,
)
from app.domain.ai.repositories.ai_request_repository import (
    AIRequestRepository,
)
from app.application.ai.services.ai_execution_service import (
    AIExecutionService,
)
from app.domain.ai.services.ai_validation_service import (
    AIValidationService,
)


class ExecuteAIRequestHandler(
    BaseHandler[
        ExecuteAIRequestCommand,
        AIResponseDTO,
    ]
):
    """
    Executes an AI request.
    """

    def __init__(
        self,
        repository: AIRequestRepository,
        execution_service: AIExecutionService,
        validation_service: AIValidationService,
    ) -> None:

        self._repository = repository
        self._execution_service = execution_service
        self._validation_service = validation_service
        self._validator = ExecuteAIRequestValidator()

    async def handle(
        self,
        request: ExecuteAIRequestCommand,
        context: HandlerContext,
    ) -> HandlerResult[AIResponseDTO]:

        validation = self._validator.validate(request)

        if not validation.is_valid:
            return HandlerResult.failure(
                message="Validation failed.",
                errors=validation.errors,
            )

        ai_request = AIMapper.dto_to_domain(
            AIMapper.command_to_dto(request)
        )

        self._validation_service.validate(
            ai_request,
        )

        response = await self._execution_service.execute(
            ai_request,
        )

        await self._repository.save(
            ai_request,
        )

        if response is None:
            return HandlerResult.failure(
                message="AI request completed without response.",
            )

        return HandlerResult.ok(
            data=AIMapper.response_to_dto(
                response,
            ),
            message="AI request executed successfully.",
        )