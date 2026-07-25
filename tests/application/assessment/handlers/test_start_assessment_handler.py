from uuid import uuid4

import pytest

from app.application.assessment.commands.start_assessment import (
    StartAssessmentCommand,
)
from app.application.assessment.handlers.start_assessment_handler import (
    StartAssessmentHandler,
)
from app.application.assessment.mappers.assessment_mapper import (
    AssessmentMapper,
)
from app.application.assessment.validators.start_assessment_validator import (
    StartAssessmentValidator,
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
        self.assessment = None

    async def save(
        self,
        assessment: Assessment,
    ) -> Assessment:

        self.assessment = assessment

        return assessment

    async def get_by_id(
        self,
        assessment_id: AssessmentId,
    ):
        return self.assessment

    async def get_by_discovery(
        self,
        discovery_session_id: DiscoverySessionId,
    ):
        return None

    async def exists(
        self,
        assessment_id: AssessmentId,
    ):
        return False

    async def delete(
        self,
        assessment: Assessment,
    ):
        return None


@pytest.mark.asyncio
async def test_start_assessment_handler_creates_assessment():

    repository = FakeAssessmentRepository()

    handler = StartAssessmentHandler(
        repository=repository,
        validator=StartAssessmentValidator(),
        mapper=AssessmentMapper(),
    )

    discovery_session_id = uuid4()

    command = StartAssessmentCommand(
        discovery_session_id=discovery_session_id,
        summary="Assessment started",
    )

    result = await handler.handle(command)

    assert result.discovery_session_id == discovery_session_id
    assert result.status == "IN_PROGRESS"
    assert result.summary == "Assessment started"