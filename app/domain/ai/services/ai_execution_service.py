from ..aggregate.ai_request import AIRequest
from ..entities.ai_response import AIResponse
from .ai_validation_service import AIValidationService


class AIExecutionService:
    """
    Coordinates the AI request lifecycle.
    """

    def __init__(
        self,
        validation_service: AIValidationService,
    ):
        self._validation_service = validation_service

    def start(
        self,
        request: AIRequest,
    ) -> None:
        """
        Prepare an AI request for execution.
        """

        self._validation_service.validate_execution(
            request
        )

        request.start()

    def complete(
        self,
        request: AIRequest,
        response: AIResponse,
    ) -> None:
        """
        Complete an AI request with a response.
        """

        request.attach_response(response)

        self._validation_service.validate_response(
            request
        )

        request.complete()

    def fail(
        self,
        request: AIRequest,
    ) -> None:
        """
        Mark an AI request as failed.
        """

        request.fail()

    def cancel(
        self,
        request: AIRequest,
    ) -> None:
        """
        Cancel an AI request.
        """

        request.cancel()