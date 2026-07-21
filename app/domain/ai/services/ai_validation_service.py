from ..aggregate.ai_request import AIRequest
from ..enums.ai_request_status import AIRequestStatus
from ..exceptions.ai_exception import AIException


class AIValidationService:
    """
    Domain service responsible for validating AI requests.
    """

    def validate_execution(
        self,
        request: AIRequest,
    ) -> None:
        """
        Validate an AI request before execution.
        """

        if request.status != AIRequestStatus.PENDING:
            raise AIException(
                "Only pending AI requests can be executed."
            )

        if not request.messages:
            raise AIException(
                "AI request must contain at least one message."
            )

    def validate_response(
        self,
        request: AIRequest,
    ) -> None:
        """
        Validate that a response exists.
        """

        if not request.has_response():
            raise AIException(
                "AI request does not contain a response."
            )