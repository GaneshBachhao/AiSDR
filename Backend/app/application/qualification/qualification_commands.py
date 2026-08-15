"""
Qualification commands.
"""

from __future__ import annotations

from app.application.common.commands.command import (
    Command,
)


class CreateQualificationCommand(Command):
    """
    Command to create a new qualification.
    """

    lead_id: str

    assessment_id: str

    status: str | None = None

    score: float | None = None

    recommendation: str | None = None


class UpdateQualificationCommand(Command):
    """
    Command to update an existing qualification.
    """

    qualification_id: str

    status: str | None = None

    score: float | None = None

    recommendation: str | None = None


class DeleteQualificationCommand(Command):
    """
    Command to delete a qualification.
    """

    qualification_id: str