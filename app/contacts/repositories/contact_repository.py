"""
Contact Repository

Persistence layer for Contact.
"""

from sqlalchemy.orm import Session

from app.contacts.schemas.contact_schema import (
    ContactCreate,
    ContactUpdate,
)

from app.models.contact import Contact


class ContactRepository:
    """
    Repository for Contact persistence.
    """

    # ======================================================
    # Create
    # ======================================================

    def create(
        self,
        db: Session,
        contact: ContactCreate,
    ) -> Contact:

        db_contact = Contact(
            **contact.model_dump()
        )

        db.add(
            db_contact,
        )

        db.commit()

        db.refresh(
            db_contact,
        )

        return db_contact

    # ======================================================
    # Update
    # ======================================================

    def update(
        self,
        db: Session,
        contact: Contact,
        update: ContactUpdate,
    ) -> Contact:

        values = update.model_dump(
            exclude_unset=True,
        )

        for key, value in values.items():

            setattr(
                contact,
                key,
                value,
            )

        db.commit()

        db.refresh(
            contact,
        )

        return contact

    # ======================================================
    # Delete
    # ======================================================

    def delete(
        self,
        db: Session,
        contact: Contact,
    ) -> None:

        db.delete(
            contact,
        )

        db.commit()

    # ======================================================
    # Queries
    # ======================================================

    def get_by_id(
        self,
        db: Session,
        contact_id: int,
    ) -> Contact | None:

        return (
            db.query(Contact)
            .filter(
                Contact.id == contact_id,
            )
            .first()
        )

    def find_by_email(
        self,
        db: Session,
        email: str,
    ) -> Contact | None:

        return (
            db.query(Contact)
            .filter(
                Contact.email == email,
            )
            .first()
        )

    def list_by_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> list[Contact]:

        return (
            db.query(Contact)
            .filter(
                Contact.lead_id == lead_id,
            )
            .all()
        )

    def get_primary_contact(
        self,
        db: Session,
        lead_id: int,
    ) -> Contact | None:

        return (
            db.query(Contact)
            .filter(
                Contact.lead_id == lead_id,
                Contact.is_primary.is_(True),
            )
            .first()
        )

    def exists(
        self,
        db: Session,
        email: str,
    ) -> bool:

        return (
            self.find_by_email(
                db,
                email,
            )
            is not None
        )

    # ======================================================
    # Primary Contact
    # ======================================================

    def set_primary(
        self,
        db: Session,
        contact: Contact,
    ) -> Contact:

        (
            db.query(Contact)
            .filter(
                Contact.lead_id == contact.lead_id,
            )
            .update(
                {
                    Contact.is_primary: False,
                }
            )
        )

        contact.is_primary = True

        db.commit()

        db.refresh(
            contact,
        )

        return contact