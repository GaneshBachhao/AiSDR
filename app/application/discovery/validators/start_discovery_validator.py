from __future__ import annotations

from app.application.common.validation.validation_result import (
    ValidationResult,
)

from app.application.discovery.commands.start_discovery import (
    StartDiscoveryCommand,
)


class StartDiscoveryValidator:
    """
    Validates StartDiscoveryCommand.
    """

    def validate(
        self,
        command: StartDiscoveryCommand,
    ) -> ValidationResult:

        result = ValidationResult()

        if not command.lead_id:
            result.add_error(
                "lead_id",
                "Lead id is required.",
            )

        return result