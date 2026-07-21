from app.emails.schemas.email_send_result_schema import (
    EmailSendResult,
)

from app.pipelines.context.pipeline_context import (
    PipelineContext,
)

from app.pipelines.stages.email_dispatch_stage import (
    EmailDispatchStage,
)


class FakeEmail:

    id = 1

    subject = "AI"

    body = "Hello"


class FakeContact:

    email = "john@test.com"


class FakeDispatchService:

    def dispatch(
        self,
        db,
        email,
        contact,
    ):

        return EmailSendResult(

            success=True,

            provider="gmail",

            message_id="MSG123",

            thread_id="THREAD1",

        )


class FakeEmailService:

    def mark_sending(
        self,
        db,
        email,
    ):

        return email

    def mark_sent(
        self,
        db,
        email,
        provider_message_id,
    ):

        return email

    def mark_failed(
        self,
        db,
        email,
    ):

        return email


def test_dispatch():

    stage = EmailDispatchStage()

    stage.dispatch_service = FakeDispatchService()

    stage.email_service = FakeEmailService()

    context = PipelineContext()

    context.db = object()

    context.email = FakeEmail()

    context.primary_contact = FakeContact()

    result = stage.execute(
        context,
    )

    assert result.email_send_result.success

    assert (

        result.email_send_result.message_id

        == "MSG123"

    )


def test_can_execute():

    stage = EmailDispatchStage()

    context = PipelineContext()

    assert stage.can_execute(context) is False

    context.db = object()

    context.email = FakeEmail()

    context.primary_contact = FakeContact()

    assert stage.can_execute(context)