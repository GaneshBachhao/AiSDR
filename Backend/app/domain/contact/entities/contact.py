"""
Contact aggregate root.

Represents a person/contact associated with a company relationship.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from app.domain.company.identifiers.company_id import (
    CompanyId,
)
from app.domain.contact.identifiers.contact_id import (
    ContactId,
)
from app.domain.contact.value_objects.email import (
    Email,
)
from app.domain.shared.base.aggregate_root import (
    AggregateRoot,
)


@dataclass(eq=False)
class Contact(AggregateRoot[ContactId]):
    """
    Aggregate root representing a business contact.

    Business invariants:
    - Contact name is mandatory.
    - Email is mandatory.
    - Email must be valid.
    - Text fields are normalized.
    """

    id: ContactId = field(
        default_factory=ContactId,
        kw_only=True,
    )

    first_name: str

    last_name: str

    email: Email

    phone: str | None = None

    job_title: str | None = None

    linkedin_url: str | None = None

    company_id: CompanyId | None = None

    is_active: bool = True


    def __post_init__(self) -> None:
        """
        Validate and normalize contact data.
        """

        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()

        self._validate_name()

        if self.phone:
            self.phone = self.phone.strip()

        if self.job_title:
            self.job_title = self.job_title.strip()

        if self.linkedin_url:
            self.linkedin_url = self.linkedin_url.strip()


    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_name(self) -> None:
        """
        Ensure contact name is valid.
        """

        if not self.first_name:
            raise ValueError(
                "Contact first name cannot be empty."
            )

        if not self.last_name:
            raise ValueError(
                "Contact last name cannot be empty."
            )


    # ---------------------------------------------------------
    # Update Operations
    # ---------------------------------------------------------

    def update_name(
        self,
        *,
        first_name: str,
        last_name: str,
    ) -> None:
        """
        Update contact name.
        """

        first_name = first_name.strip()
        last_name = last_name.strip()

        if not first_name:
            raise ValueError(
                "Contact first name cannot be empty."
            )

        if not last_name:
            raise ValueError(
                "Contact last name cannot be empty."
            )

        self.first_name = first_name
        self.last_name = last_name

        self.touch()


    def update_email(
        self,
        email: Email,
    ) -> None:
        """
        Update contact email.
        """

        self.email = email

        self.touch()


    def update_phone(
        self,
        phone: str | None,
    ) -> None:
        """
        Update contact phone.
        """

        self.phone = (
            phone.strip()
            if phone
            else None
        )

        self.touch()


    def update_job_title(
        self,
        job_title: str | None,
    ) -> None:
        """
        Update contact designation.
        """

        self.job_title = (
            job_title.strip()
            if job_title
            else None
        )

        self.touch()


    def update_linkedin_url(
        self,
        linkedin_url: str | None,
    ) -> None:
        """
        Update LinkedIn profile URL.
        """

        self.linkedin_url = (
            linkedin_url.strip()
            if linkedin_url
            else None
        )

        self.touch()


    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def activate(self) -> None:
        """
        Activate contact.
        """

        self.is_active = True

        self.touch()


    def deactivate(self) -> None:
        """
        Deactivate contact.
        """

        self.is_active = False

        self.touch()