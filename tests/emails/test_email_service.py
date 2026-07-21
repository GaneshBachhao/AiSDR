"""
Tests for EmailService.
"""

from types import SimpleNamespace

from app.emails.enums.email_direction import (
    EmailDirection,
)

from app.emails.enums.email_status import (
    EmailStatus,
)

from app.emails.schemas.email_schema import (
    EmailCreate,
)

from app.emails.services.email_service import (
    EmailService,
)


# ==========================================================
# Fake Repository
# ==========================================================


class FakeRepository:
    """
    Fake EmailRepository for unit testing.
    """

    def __init__(self):

        self.email = None

    def create(
        self,
        db,
        email,
    ):

        self.email = SimpleNamespace(

            id=1,

            lead_id=email.lead_id,

            contact_id=email.contact_id,

            subject=email.subject,

            body=email.body,

            provider=email.provider,

            direction=email.direction,

            status=EmailStatus.DRAFT,

            provider_message_id=None,

            thread_id=None,

            external_reference=None,

            error_message=None,

        )

        return self.email

    def update(
        self,
        db,
        entity,
        update,
    ):

        values = update.model_dump(

            exclude_none=True,

            exclude_unset=True,

        )

        for field, value in values.items():

            setattr(

                entity,

                field,

                value,

            )

        return entity

    def get_by_id(
        self,
        db,
        email_id,
    ):

        return self.email

    def list_by_lead(
        self,
        db,
        lead_id,
    ):

        return [self.email]


# ==========================================================
# Helpers
# ==========================================================


def build_email_create():

    return EmailCreate(

        lead_id=1,

        contact_id=1,

        subject="AI Automation",

        body="Hello from AI SDR.",

        provider="gmail",

        direction=EmailDirection.OUTBOUND,

    )


# ==========================================================
# Tests
# ==========================================================


def test_create_draft():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    assert email.id == 1

    assert email.lead_id == 1

    assert email.contact_id == 1

    assert email.subject == "AI Automation"

    assert email.status == EmailStatus.DRAFT


def test_queue():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.queue(

        None,

        email,

    )

    assert result.status == EmailStatus.QUEUED


def test_mark_sending():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_sending(

        None,

        email,

    )

    assert result.status == EmailStatus.SENDING


def test_mark_sent():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_sent(

        None,

        email,

        "gmail-123",

    )

    assert result.status == EmailStatus.SENT

    assert result.provider_message_id == "gmail-123"


def test_mark_delivered():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_delivered(

        None,

        email,

    )

    assert result.status == EmailStatus.DELIVERED


def test_mark_opened():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_opened(

        None,

        email,

    )

    assert result.status == EmailStatus.OPENED


def test_mark_clicked():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_clicked(

        None,

        email,

    )

    assert result.status == EmailStatus.CLICKED


def test_mark_replied():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_replied(

        None,

        email,

    )

    assert result.status == EmailStatus.REPLIED


def test_mark_failed():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_failed(

        None,

        email,

    )

    assert result.status == EmailStatus.FAILED


def test_mark_bounced():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.mark_bounced(

        None,

        email,

    )

    assert result.status == EmailStatus.BOUNCED


def test_cancel():

    service = EmailService(

        repository=FakeRepository(),

    )

    email = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.cancel(

        None,

        email,

    )

    assert result.status == EmailStatus.CANCELLED


def test_get():

    repository = FakeRepository()

    service = EmailService(

        repository=repository,

    )

    created = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.get(

        None,

        created.id,

    )

    assert result == created


def test_list_by_lead():

    repository = FakeRepository()

    service = EmailService(

        repository=repository,

    )

    created = service.create_draft(

        None,

        build_email_create(),

    )

    result = service.list_by_lead(

        None,

        created.lead_id,

    )

    assert len(result) == 1

    assert result[0] == created