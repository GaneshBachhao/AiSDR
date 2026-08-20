"""
Assessment commands.

Architecture Freeze v5.0
Application command contracts for the Assessment aggregate.
"""

from __future__ import annotations

from app.application.common.commands.command import Command


class CreateAssessmentCommand(Command):
    """Command to create a new assessment."""

    discovery_id: str


class StartAssessmentCommand(Command):
    """Command to start an assessment."""

    assessment_id: str


class CompleteAssessmentCommand(Command):
    """Command to complete an assessment."""

    assessment_id: str
    summary: str | None = None


class UpdateAssessmentCommand(Command):
    """Command to update an existing assessment."""

    assessment_id: str
    summary: str | None = None
    maturity_level: str | None = None
    readiness_score: float | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    opportunities: str | None = None
    risks: str | None = None


class DeleteAssessmentCommand(Command):
    """Command to delete an assessment."""

    assessment_id: str
