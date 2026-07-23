from uuid import uuid4

from app.application.recommendation.commands.generate_recommendation import (
    GenerateRecommendationCommand,
)
from app.application.recommendation.mappers.recommendation_mapper import (
    RecommendationMapper,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.recommendation.entities.recommendation import (
    Recommendation,
)


def test_command_to_assessment_id():
    assessment_uuid = uuid4()

    command = GenerateRecommendationCommand(
        assessment_id=assessment_uuid,
    )

    identifier = RecommendationMapper.command_to_assessment_id(
        command,
    )

    assert isinstance(
        identifier,
        AssessmentId,
    )

    assert identifier.value == assessment_uuid


def test_domain_to_dto():
    assessment_id = AssessmentId()

    recommendation = Recommendation(
        assessment_id=assessment_id,
    )

    dto = RecommendationMapper.domain_to_dto(
        recommendation,
    )

    assert dto.id == recommendation.id.value

    assert dto.assessment_id == assessment_id.value

    assert dto.status == recommendation.status.value

    assert dto.solutions == []

    assert dto.roadmap_phases == []