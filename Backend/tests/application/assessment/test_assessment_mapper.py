"""
Tests for Assessment application mapper.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from app.application.assessment.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.dto.assessment_request import (
    CreateAssessmentRequestDTO,
    UpdateAssessmentRequestDTO,
)
from app.domain.assessment.entities.assessment import Assessment


class TestAssessmentMapper:
    """
    Tests for AssessmentMapper.
    """

    def test_to_create_command(self) -> None:
        dto = CreateAssessmentRequestDTO(
            discovery_id="discovery-123",
        )

        command = AssessmentMapper.to_create_command(dto)

        assert command.discovery_id == "discovery-123"

    def test_to_update_command(self) -> None:
        dto = UpdateAssessmentRequestDTO(
            summary="Assessment summary",
            maturity_level="Advanced",
            readiness_score=92.5,
            strengths="Strong architecture",
            weaknesses="Limited automation",
            opportunities="Expand integrations",
            risks="Resource constraints",
        )

        command = AssessmentMapper.to_update_command(
            assessment_id="assessment-123",
            dto=dto,
        )

        assert command.assessment_id == "assessment-123"
        assert command.summary == dto.summary
        assert command.maturity_level == dto.maturity_level
        assert command.readiness_score == dto.readiness_score
        assert command.strengths == dto.strengths
        assert command.weaknesses == dto.weaknesses
        assert command.opportunities == dto.opportunities
        assert command.risks == dto.risks

    def test_to_create_response(self) -> None:
        assessment = self._assessment()

        response = AssessmentMapper.to_create_response(
            assessment,
        )

        self._assert_full_response(response)

    def test_to_get_response(self) -> None:
        assessment = self._assessment()

        response = AssessmentMapper.to_get_response(
            assessment,
        )

        self._assert_full_response(response)

    def test_to_update_response(self) -> None:
        assessment = self._assessment()

        response = AssessmentMapper.to_update_response(
            assessment,
        )

        self._assert_full_response(response)

    def test_to_list_response(self) -> None:
        assessment = self._assessment()

        response = AssessmentMapper.to_list_response(
            assessment,
        )

        assert response.assessment_id == assessment.id.value
        assert response.discovery_id == assessment.discovery_id.value
        assert response.summary == "Assessment summary"
        assert response.maturity_level == "Advanced"
        assert response.readiness_score == 92.5

    @staticmethod
    def _assessment() -> SimpleNamespace:
        assessment = SimpleNamespace()

        assessment.id = SimpleNamespace(value=uuid4())
        assessment.discovery_id = SimpleNamespace(value=uuid4())

        assessment.summary = "Assessment summary"

        assessment.maturity_level = SimpleNamespace(name="Advanced")

        assessment.score = SimpleNamespace(overall_score=92.5)

        return assessment

    @staticmethod
    def _assert_full_response(response) -> None:
        assert response.assessment_id is not None
        assert response.discovery_id is not None
        assert response.summary == "Assessment summary"
        assert response.maturity_level == "Advanced"
        assert response.readiness_score == 92.5

        # Current mapper implementation returns None for SWOT fields.
        assert response.strengths is None
        assert response.weaknesses is None
        assert response.opportunities is None
        assert response.risks is None