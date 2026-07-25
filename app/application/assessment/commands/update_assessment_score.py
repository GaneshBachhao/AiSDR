# app/application/assessment/commands/update_assessment_score.py

"""
Update Assessment Score command.
"""

from __future__ import annotations

from uuid import UUID

from app.application.common.commands.command import (
    Command,
)


class UpdateAssessmentScoreCommand(Command):
    """
    Request to update an assessment score.
    """

    assessment_id: UUID

    overall_score: float

    strategy_score: float = 0.0

    process_score: float = 0.0

    technology_score: float = 0.0

    data_score: float = 0.0

    people_score: float = 0.0