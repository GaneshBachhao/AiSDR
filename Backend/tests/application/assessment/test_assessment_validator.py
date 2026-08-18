"""
Tests for Assessment validator.
"""

from __future__ import annotations

from app.application.assessment.assessment_commands import (
    CreateAssessmentCommand,
    UpdateAssessmentCommand,
)
from app.application.assessment.assessment_validator import (
    AssessmentValidator,
)


class TestAssessmentValidator:
    """
    Tests for AssessmentValidator.
    """

    def test_validate_create_valid_command(self) -> None:
        command = CreateAssessmentCommand(
            discovery_id="discovery-123",
        )

        result = AssessmentValidator.validate_create(command)

        assert result.is_valid

    def test_validate_create_missing_discovery_id(self) -> None:
        command = CreateAssessmentCommand(
            discovery_id="",
        )

        result = AssessmentValidator.validate_create(command)

        assert not result.is_valid
        assert result.has_error("discovery_id")

    def test_validate_update_valid_command(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
            readiness_score=85,
        )

        result = AssessmentValidator.validate_update(command)

        assert result.is_valid

    def test_validate_update_missing_assessment_id(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="",
        )

        result = AssessmentValidator.validate_update(command)

        assert not result.is_valid
        assert result.has_error("assessment_id")

    def test_validate_update_readiness_score_below_range(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
            readiness_score=-1,
        )

        result = AssessmentValidator.validate_update(command)

        assert not result.is_valid
        assert result.has_error("readiness_score")

    def test_validate_update_readiness_score_above_range(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
            readiness_score=101,
        )

        result = AssessmentValidator.validate_update(command)

        assert not result.is_valid
        assert result.has_error("readiness_score")

    def test_validate_update_readiness_score_lower_boundary(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
            readiness_score=0,
        )

        result = AssessmentValidator.validate_update(command)

        assert result.is_valid

    def test_validate_update_readiness_score_upper_boundary(self) -> None:
        command = UpdateAssessmentCommand(
            assessment_id="assessment-123",
            readiness_score=100,
        )

        result = AssessmentValidator.validate_update(command)

        assert result.is_valid
