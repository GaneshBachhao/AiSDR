"""
Discovery application validator.

Architecture Freeze v5.0
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.validation.validation_result import ValidationResult
from app.application.discovery.discovery_commands import (
    CreateDiscoveryCommand,
    DeleteDiscoveryCommand,
    UpdateDiscoveryCommand,
)
from app.application.discovery.discovery_queries import (
    GetDiscoveryQuery,
    ListDiscoveryQuery,
    SearchDiscoveryQuery,
)
from app.domain.discovery.enums.discovery_status import DiscoveryStatus


class DiscoveryValidator:
    """Validate Discovery commands and queries."""

    @staticmethod
    def _validate_uuid(
        value: str,
        field: str,
        result: ValidationResult,
    ) -> None:
        if not value.strip():
            result.add_error(
                field,
                f"{field.replace('_', ' ').title()} is required.",
            )
            return

        try:
            UUID(value.strip())
        except (ValueError, AttributeError):
            result.add_error(
                field,
                f"{field.replace('_', ' ').title()} must be a valid UUID.",
            )

    @staticmethod
    def _validate_status(
        value: str,
        result: ValidationResult,
    ) -> None:
        """
        Validate a Discovery lifecycle status against
        the domain-owned DiscoveryStatus enum.
        """
        if not value.strip():
            result.add_error(
                "status",
                "Status cannot be empty.",
            )
            return

        try:
            DiscoveryStatus(value.strip().upper())
        except ValueError:
            result.add_error(
                "status",
                "Invalid discovery status.",
            )

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    @staticmethod
    def validate_create(
        command: CreateDiscoveryCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        DiscoveryValidator._validate_uuid(
            command.lead_id,
            "lead_id",
            result,
        )

        return result

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    @staticmethod
    def validate_update(
        command: UpdateDiscoveryCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        DiscoveryValidator._validate_uuid(
            command.discovery_id,
            "discovery_id",
            result,
        )

        if command.status is not None:
            DiscoveryValidator._validate_status(
                command.status,
                result,
            )

        return result

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    @staticmethod
    def validate_delete(
        command: DeleteDiscoveryCommand,
    ) -> ValidationResult:
        result = ValidationResult()

        DiscoveryValidator._validate_uuid(
            command.discovery_id,
            "discovery_id",
            result,
        )

        return result

    # ---------------------------------------------------------
    # Get
    # ---------------------------------------------------------

    @staticmethod
    def validate_get(
        query: GetDiscoveryQuery,
    ) -> ValidationResult:
        result = ValidationResult()

        DiscoveryValidator._validate_uuid(
            query.discovery_id,
            "discovery_id",
            result,
        )

        return result

    # ---------------------------------------------------------
    # List
    # ---------------------------------------------------------

    @staticmethod
    def validate_list(
        query: ListDiscoveryQuery,
    ) -> ValidationResult:
        result = ValidationResult()

        if query.skip < 0:
            result.add_error(
                "skip",
                "Skip cannot be negative.",
            )

        if query.limit < 1:
            result.add_error(
                "limit",
                "Limit must be greater than zero.",
            )

        return result

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    @staticmethod
    def validate_search(
        query: SearchDiscoveryQuery,
    ) -> ValidationResult:
        result = ValidationResult()

        if not query.search_text.strip():
            result.add_error(
                "search_text",
                "Search text is required.",
            )

        if query.skip < 0:
            result.add_error(
                "skip",
                "Skip cannot be negative.",
            )

        if query.limit < 1:
            result.add_error(
                "limit",
                "Limit must be greater than zero.",
            )

        return result