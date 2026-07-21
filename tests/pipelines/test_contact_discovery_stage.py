from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.contact_discovery_stage import (
    ContactDiscoveryStage,
)


class FakeContact:

    def __init__(self):

        self.id = 1

        self.email = "john@test.com"


class FakeLead:

    id = 99


class FakeContactService:

    def list_by_lead(
        self,
        db,
        lead_id,
    ):

        return [
            FakeContact(),
        ]

    def get_primary(
        self,
        db,
        lead_id,
    ):

        return FakeContact()


def test_contact_discovery():

    stage = ContactDiscoveryStage()

    stage.contact_service = (
        FakeContactService()
    )

    context = PipelineContext()

    context.db = object()

    context.lead = FakeLead()

    result = stage.execute(
        context,
    )

    assert len(result.contacts) == 1

    assert (
        result.primary_contact.email
        == "john@test.com"
    )


def test_can_execute():

    stage = ContactDiscoveryStage()

    context = PipelineContext()

    assert stage.can_execute(context) is False

    context.db = object()

    context.lead = FakeLead()

    assert stage.can_execute(context) is True