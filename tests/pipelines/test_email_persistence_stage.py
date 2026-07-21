from app.ai.schemas.generated_email_schema import (
    GeneratedEmail,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.email_persistence_stage import (
    EmailPersistenceStage,
)


class FakeLead:

    id = 1


class FakeContact:

    id = 10


class FakeEmail:

    id = 99

    subject = "AI Opportunity"


class FakeEmailService:

    def create_draft(
        self,
        db,
        request,
    ):

        return FakeEmail()


def test_create_email_draft():

    stage = EmailPersistenceStage()

    stage.service = FakeEmailService()

    context = PipelineContext()

    context.db = object()

    context.lead = FakeLead()

    context.primary_contact = FakeContact()

    context.generated_email = GeneratedEmail(

        subject="AI Opportunity",

        body="Hello",

    )

    result = stage.execute(
        context,
    )

    assert result.email.id == 99

    assert result.email.subject == "AI Opportunity"


def test_can_execute():

    stage = EmailPersistenceStage()

    context = PipelineContext()

    assert stage.can_execute(context) is False

    context.db = object()

    context.lead = FakeLead()

    context.primary_contact = FakeContact()

    context.generated_email = GeneratedEmail(

        subject="Hello",

        body="World",

    )

    assert stage.can_execute(context) is True