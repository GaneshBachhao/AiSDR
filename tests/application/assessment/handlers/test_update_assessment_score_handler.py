from uuid import uuid4

import pytest

from app.application.assessment.commands.update_assessment_score import (
    UpdateAssessmentScoreCommand,
)
from app.application.assessment.handlers.update_assessment_score_handler import (
    UpdateAssessmentScoreHandler,
)
from app.application.assessment.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.validators.update_assessment_score_validator import (
    UpdateAssessmentScoreValidator,
)
from app.domain.assessment.entities.assessment import (
    Assessment,
)
from app.domain.assessment.identifiers.assessment_id import (
    AssessmentId,
)
from app.domain.assessment.repositories.assessment_repository import (
    AssessmentRepository,
)
from app.domain.discovery.identifiers.discovery_session_id import (
    DiscoverySessionId,
)


class FakeAssessmentRepository(
    AssessmentRepository,
):

    def __init__(self):

        self.assessment = Assessment(
            discovery_session_id=DiscoverySessionId(),
        )

    async def save(
        self,
        assessment: Assessment,
    ) -> Assessment:

        self.assessment = assessment

        return assessment

    async def get_by_id(
        self,
        assessment_id: AssessmentId,
    ) -> Assessment | None:

        return self.assessment

    async def get_by_discovery(
        self,
        discovery_session_id: DiscoverySessionId,
    ) -> Assessment | None:

        return None

    async def exists(
        self,
        assessment_id: AssessmentId,
    ) -> bool:

        return True

    async def delete(
        self,
        assessment: Assessment,
    ) -> None:

        return None


@pytest.mark.asyncio
async def test_update_assessment_score_handler_updates_score():

    repository = FakeAssessmentRepository()

    handler = UpdateAssessmentScoreHandler(
        repository=repository,
        validator=UpdateAssessmentScoreValidator(),
        mapper=AssessmentMapper(),
    )

    command = UpdateAssessmentScoreCommand(
        assessment_id=repository.assessment.id.value,
        overall_score=82,
    )

    result = await handler.handle(command)

    assert result.score == 82

    assert result.maturity_level == "OPTIMIZED"