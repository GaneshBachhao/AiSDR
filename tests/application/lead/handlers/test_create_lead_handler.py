from unittest.mock import AsyncMock

import pytest

from app.application.lead.commands.create_lead import (
    CreateLeadCommand,
)

from app.application.lead.handlers.create_lead_handler import (
    CreateLeadHandler,
)

from app.application.lead.mappers.lead_mapper import (
    LeadMapper,
)

from app.application.lead.validators.create_lead_validator import (
    CreateLeadValidator,
)


class FakeLeadRepository:
    def __init__(self):
        self.add = AsyncMock()

        self.saved_lead = None

    async def get_by_id(self, lead_id):
        return self.saved_lead


@pytest.mark.asyncio
async def test_create_lead_handler_creates_lead():

    repository = FakeLeadRepository()

    handler = CreateLeadHandler(
        repository=repository,
        validator=CreateLeadValidator(),
        mapper=LeadMapper(),
    )

    command = CreateLeadCommand(
        company_name="OpenAI",
        contact_name="John Smith",
        email="john@openai.com",
        phone="1234567890",
        website="https://openai.com",
    )

    result = await handler.handle(command)

    assert result.company_name == "OpenAI"
    assert result.contact_name == "John Smith"
    assert result.email == "john@openai.com"

    repository.add.assert_called_once()