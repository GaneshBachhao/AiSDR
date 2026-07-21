"""
Email Service

Business logic for Email lifecycle management.
"""

from sqlalchemy.orm import Session

from app.emails.enums.email_status import (
    EmailStatus,
)

from app.emails.repositories.email_repository import (
    EmailRepository,
)

from app.emails.schemas.email_schema import (
    EmailCreate,
    EmailUpdate,
)

from app.models.email import Email


class EmailService:
    """
    Business service for Email lifecycle.
    """

    def __init__(
        self,
        repository: EmailRepository | None = None,
    ):

        self.repository = (
            repository
            if repository is not None
            else EmailRepository()
        )

    # ======================================================
    # Create
    # ======================================================

    def create_draft(
        self,
        db: Session,
        email: EmailCreate,
    ) -> Email:

        return self.repository.create(
            db,
            email,
        )

    # ======================================================
    # Queue
    # ======================================================

    def queue(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.QUEUED,
            ),
        )

    # ======================================================
    # Sending
    # ======================================================

    def mark_sending(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.SENDING,
            ),
        )

    # ======================================================
    # Sent
    # ======================================================

    def mark_sent(
        self,
        db: Session,
        email: Email,
        provider_message_id: str,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.SENT,
                provider_message_id=provider_message_id,
            ),
        )

    # ======================================================
    # Delivery
    # ======================================================

    def mark_delivered(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.DELIVERED,
            ),
        )

    # ======================================================
    # Tracking
    # ======================================================

    def mark_opened(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.OPENED,
            ),
        )

    def mark_clicked(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.CLICKED,
            ),
        )

    def mark_replied(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.REPLIED,
            ),
        )

    # ======================================================
    # Failure
    # ======================================================

    def mark_failed(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.FAILED,
            ),
        )

    def mark_bounced(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.BOUNCED,
            ),
        )

    def cancel(
        self,
        db: Session,
        email: Email,
    ) -> Email:

        return self.repository.update(
            db,
            email,
            EmailUpdate(
                status=EmailStatus.CANCELLED,
            ),
        )

    # ======================================================
    # Queries
    # ======================================================

    def get(
        self,
        db: Session,
        email_id: int,
    ) -> Email | None:

        return self.repository.get_by_id(
            db,
            email_id,
        )

    def list_by_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> list[Email]:

        return self.repository.list_by_lead(
            db,
            lead_id,
        )