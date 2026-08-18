"""
Tests for Assessment commands.
"""

from __future__ import annotations

from app.application.assessment.assessment_commands import (
    CreateAssessmentCommand,
    DeleteAssessmentCommand,
    UpdateAssessmentCommand,
)


class TestCreateAssessmentCommand:
    """
    Tests for CreateAssessmentCommand.
    """

    def test_create_assessment_command(self) -> None:
        command = CreateAssessmentCommand(
            discovery_id="discovery-123",
        )

        assert command.discovery_id == "discovery-123"


class TestUpdateAssessmentCommand:
    """
    Tests for UpdateAssessmentCommand.
    """

    def test_update_assessment_command_all_fields(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
            summary="Assessment summary",
            maturity_level="Advanced",
            readiness_score=92.5,
            strengths="Strong architecture",
            weaknesses="Limited automation",
            opportunities="Expand integrations",
            risks="Resource constraints",
        )

        assert command.assessment_id == "assessment-123"
        assert command.summary == "Assessment summary"
        assert command.maturity_level == "Advanced"
        assert command.readiness_score == 92.5
        assert command.strengths == "Strong architecture"
        assert command.weaknesses == "Limited automation"
        assert command.opportunities == "Expand integrations"
        assert command.risks == "Resource constraints"

    def test_update_assessment_command_required_only(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
        )

        assert command.assessment_id == "assessment-123"
        assert command.summary is None
        assert command.maturity_level is None
        assert command.readiness_score is None
        assert command.strengths is None
        assert command.weaknesses is None
        assert command.opportunities is None
        assert command.risks is None


class TestDeleteAssessmentCommand:
    """
    Tests for DeleteAssessmentCommand.
    """

    def test_delete_assessment_command(self) -> None:
        command = DeleteAssessmentCommand(
            assessment_id="assessment-123",
        )

        assert command.assessment_id == "assessment-123"
