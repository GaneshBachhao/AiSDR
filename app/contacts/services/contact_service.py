"""
Contact Service

Business logic for Contact lifecycle management.
"""

from sqlalchemy.orm import Session

from app.contacts.repositories.contact_repository import (
    ContactRepository,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
    ContactUpdate,
)

from app.models.contact import Contact


class ContactService:
    """
    Business service for Contact lifecycle.
    """

    def __init__(
        self,
        repository: ContactRepository | None = None,
    ):

        self.repository = (
            repository
            if repository is not None
            else ContactRepository()
        )

    # ======================================================
    # Create
    # ======================================================

    def create(
        self,
        db: Session,
        contact: ContactCreate,
    ) -> Contact:

        return self.repository.create(
            db,
            contact,
        )

    # ======================================================
    # Update
    # ======================================================

    def update(
        self,
        db: Session,
        contact: Contact,
        update: ContactUpdate,
    ) -> Contact:

        return self.repository.update(
            db,
            contact,
            update,
        )

    # ======================================================
    # Delete
    # ======================================================

    def delete(
        self,
        db: Session,
        contact: Contact,
    ) -> None:

        self.repository.delete(
            db,
            contact,
        )

    # ======================================================
    # Queries
    # ======================================================

    def get(
        self,
        db: Session,
        contact_id: int,
    ) -> Contact | None:

        return self.repository.get_by_id(
            db,
            contact_id,
        )

    def find_by_email(
        self,
        db: Session,
        email: str,
    ) -> Contact | None:

        return self.repository.find_by_email(
            db,
            email,
        )

    def exists(
        self,
        db: Session,
        email: str,
    ) -> bool:

        return self.repository.exists(
            db,
            email,
        )

    def list_by_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> list[Contact]:

        return self.repository.list_by_lead(
            db,
            lead_id,
        )

    def get_primary(
        self,
        db: Session,
        lead_id: int,
    ) -> Contact | None:

        return self.repository.get_primary_contact(
            db,
            lead_id,
        )

    # ======================================================
    # Primary Contact
    # ======================================================

    def set_primary(
        self,
        db: Session,
        contact: Contact,
    ) -> Contact:

        return self.repository.set_primary(
            db,
            contact,
        )