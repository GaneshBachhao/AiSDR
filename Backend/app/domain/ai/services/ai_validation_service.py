from app.domain.ai.aggregates.ai_request import AIRequest


class AIValidationService:
    """
    Domain validation service for AI requests.
    """

    @staticmethod
    def validate(
        request: AIRequest,
    ) -> None:
        """
        Validate an AI request before execution.
        """

        if not request.prompt.value:
            raise ValueError("Prompt cannot be empty.")

        if not request.provider.value:
            raise ValueError("Provider is required.")

        if not request.model.value:
            raise ValueError("Model is required.")

        if not request.can_execute:
            raise ValueError("AI request cannot be executed.")
