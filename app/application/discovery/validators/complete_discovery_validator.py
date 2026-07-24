from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)

from app.application.discovery.commands.complete_discovery import (
    CompleteDiscoveryCommand,
)


class CompleteDiscoveryValidator:
    """
    Validates CompleteDiscoveryCommand.
    """

    def validate(
        self,
        command: CompleteDiscoveryCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if not command.discovery_session_id:
            result.add_error(
                "discovery_session_id",
                "Discovery session id is required.",
            )

        return result