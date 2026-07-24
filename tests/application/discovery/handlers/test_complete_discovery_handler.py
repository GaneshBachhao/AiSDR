from unittest.mock import AsyncMock

import pytest
from uuid import uuid4

from app.application.discovery.commands.complete_discovery import (
    CompleteDiscoveryCommand,
)

from app.application.discovery.handlers.complete_discovery_handler import (
    CompleteDiscoveryHandler,
)

from app.application.discovery.mappers.discovery_mapper import (
    DiscoveryMapper,
)

from app.application.discovery.validators.complete_discovery_validator import (
    CompleteDiscoveryValidator,
)

from app.domain.discovery.entities.discovery_session import (
    DiscoverySession,
)

from app.domain.lead.identifiers.lead_id import (
    LeadId,
)


class FakeDiscoveryRepository:
    """
    Fake repository for application testing.
    """

    def __init__(
        self,
        session: DiscoverySession,
    ):
        self.session = session

        self.get_by_id = AsyncMock(
            return_value=session
        )

        self.update = AsyncMock()


@pytest.mark.asyncio
async def test_complete_discovery_handler_completes_session():

    session = DiscoverySession(
        lead_id=LeadId(),
    )

    session.start()

    repository = FakeDiscoveryRepository(
        session
    )

    handler = CompleteDiscoveryHandler(
        repository=repository,
        validator=CompleteDiscoveryValidator(),
        mapper=DiscoveryMapper(),
    )

    command = CompleteDiscoveryCommand(
        discovery_session_id=session.id.value,
        summary="Discovery completed successfully.",
    )

    result = await handler.handle(command)

    assert result.summary == (
        "Discovery completed successfully."
    )

    assert result.status == "Completed"

    repository.get_by_id.assert_called_once()

    repository.update.assert_called_once()