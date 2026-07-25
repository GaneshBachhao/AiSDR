from uuid import uuid4

import pytest

from app.application.assessment.commands.add_finding import (
    AddFindingCommand,
)
from app.application.assessment.handlers.add_finding_handler import (
    AddFindingHandler,
)
from app.application.assessment.mappers.finding_mapper import (
    FindingMapper,
)
from app.application.assessment.validators.add_finding_validator import (
    AddFindingValidator,
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
async def test_add_finding_handler_adds_finding():

    repository = FakeAssessmentRepository()

    handler = AddFindingHandler(
        repository=repository,
        validator=AddFindingValidator(),
        mapper=FindingMapper(),
    )

    command = AddFindingCommand(
        assessment_id=repository.assessment.id.value,
        title="Manual Sales Process",
        description="Sales representatives spend hours on repetitive tasks.",
        finding_type="OPPORTUNITY",
        severity=4,
        recommendation_hint="Automate lead qualification.",
    )

    result = await handler.handle(command)

    assert result.title == "Manual Sales Process"
    assert result.severity == 4
    assert result.finding_type == "OPPORTUNITY"

    assert len(
        repository.assessment.findings,
    ) == 1