"""
Email Repository

Database operations for Email entities.
"""

from sqlalchemy.orm import Session

from app.models.email import Email

from app.emails.schemas.email_schema import (
    EmailCreate,
    EmailUpdate,
)


class EmailRepository:
    """
    Repository for Email persistence.
    """

    def create(
        self,
        db: Session,
        email: EmailCreate,
    ) -> Email:

        entity = Email(
            **email.model_dump()
        )

        db.add(entity)

        db.commit()

        db.refresh(entity)

        return entity

    def get_by_id(
        self,
        db: Session,
        email_id: int,
    ) -> Email | None:

        return (
            db.query(Email)
            .filter(
                Email.id == email_id
            )
            .first()
        )

    def get_by_provider_message_id(
        self,
        db: Session,
        provider_message_id: str,
    ) -> Email | None:

        return (
            db.query(Email)
            .filter(
                Email.provider_message_id
                == provider_message_id
            )
            .first()
        )

    def list_by_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> list[Email]:

        return (
            db.query(Email)
            .filter(
                Email.lead_id == lead_id
            )
            .order_by(
                Email.created_at.desc()
            )
            .all()
        )

    def update(
        self,
        db: Session,
        entity: Email,
        update: EmailUpdate,
    ) -> Email:

        values = update.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in values.items():

            setattr(
                entity,
                field,
                value,
            )

        db.commit()

        db.refresh(entity)

        return entity

    def delete(
        self,
        db: Session,
        entity: Email,
    ) -> None:

        db.delete(entity)

        db.commit()