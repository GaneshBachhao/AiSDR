from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.application.discovery.commands.add_discovery_response import (
    AddDiscoveryResponseCommand,
)

from app.application.discovery.handlers.add_discovery_response_handler import (
    AddDiscoveryResponseHandler,
)

from app.application.discovery.mappers.discovery_response_mapper import (
    DiscoveryResponseMapper,
)

from app.application.discovery.validators.add_discovery_response_validator import (
    AddDiscoveryResponseValidator,
)

from app.domain.discovery.entities.discovery_session import (
    DiscoverySession,
)

from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class FakeDiscoveryRepository:
    """
    Fake repository for application layer testing.
    """

    def __init__(
        self,
        session: DiscoverySession,
    ):
        self.session = session

        self.get_by_id = AsyncMock(
            return_value=session,
        )

        self.update = AsyncMock()


@pytest.mark.asyncio
async def test_add_discovery_response_handler_adds_response():

    discovery_session = DiscoverySession(
        lead_id=LeadId(),
    )

    repository = FakeDiscoveryRepository(
        discovery_session,
    )

    handler = AddDiscoveryResponseHandler(
        repository=repository,
        validator=AddDiscoveryResponseValidator(),
        mapper=DiscoveryResponseMapper(),
    )

    command = AddDiscoveryResponseCommand(
        discovery_session_id=discovery_session.id.value,
        question_id="q1",
        question="What business problem are you solving?",
        answer="We need AI automation for sales.",
        response_type="Text",
        confidence=0.9,
        remarks="Captured during discovery call",
    )

    result = await handler.handle(command)

    assert result.question_id == "q1"

    assert result.question == (
        "What business problem are you solving?"
    )

    assert result.answer == (
        "We need AI automation for sales."
    )

    assert result.response_type == "Text"

    assert result.confidence == 0.9

    assert result.remarks == (
        "Captured during discovery call"
    )

    assert len(discovery_session.responses) == 1

    repository.get_by_id.assert_called_once()

    repository.update.assert_called_once()