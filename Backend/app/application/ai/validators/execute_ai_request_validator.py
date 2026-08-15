"""
Execute AI Request Validator
"""

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)
from app.application.common.validation.validation_result import (
    ValidationResult,
)
from app.application.common.validation.validator import (
    Validator,
)


class ExecuteAIRequestValidator(
    Validator[ExecuteAIRequestCommand],
):
    """
    Validates ExecuteAIRequestCommand.
    """

    def validate(
        self,
        command: ExecuteAIRequestCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if not command.provider.strip():
            result.add_error(
                field="provider",
                message="Provider is required.",
            )

        if not command.model.strip():
            result.add_error(
                field="model",
                message="Model is required.",
            )

        if not command.prompt.strip():
            result.add_error(
                field="prompt",
                message="Prompt is required.",
            )

        return result