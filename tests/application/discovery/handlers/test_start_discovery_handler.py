from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.application.discovery.commands.start_discovery import (
    StartDiscoveryCommand,
)

from app.application.discovery.handlers.start_discovery_handler import (
    StartDiscoveryHandler,
)

from app.application.discovery.mappers.discovery_mapper import (
    DiscoveryMapper,
)

from app.application.discovery.validators.start_discovery_validator import (
    StartDiscoveryValidator,
)


class FakeDiscoveryRepository:
    """
    Fake repository for application layer testing.
    Infrastructure is not involved.
    """

    def __init__(self):
        self.add = AsyncMock()


@pytest.mark.asyncio
async def test_start_discovery_handler_creates_session():

    repository = FakeDiscoveryRepository()

    handler = StartDiscoveryHandler(
        repository=repository,
        validator=StartDiscoveryValidator(),
        mapper=DiscoveryMapper(),
    )

    lead_id = uuid4()

    command = StartDiscoveryCommand(
        lead_id=lead_id,
        company_id="company-001",
    )

    result = await handler.handle(command)

    assert result.lead_id == lead_id
    assert result.company_id == "company-001"

    # Domain enum uses business language
    assert result.status == "In Progress"

    repository.add.assert_called_once()