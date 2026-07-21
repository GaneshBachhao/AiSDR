"""
Tests for ContactService.
"""

from app.contacts.repositories.contact_repository import (
    ContactRepository,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
    ContactUpdate,
)

from app.contacts.services.contact_service import (
    ContactService,
)


def create_contact(
    service,
    db_session,
    email="john@example.com",
    lead_id=1,
    primary=False,
):

    return service.create(
        db_session,
        ContactCreate(
            lead_id=lead_id,
            full_name="John Doe",
            email=email,
            is_primary=primary,
        ),
    )


# ==========================================================
# Create
# ==========================================================


def test_create(
    db_session,
):

    service = ContactService()

    contact = create_contact(
        service,
        db_session,
    )

    assert contact.id is not None


# ==========================================================
# Get
# ==========================================================


def test_get(
    db_session,
):

    service = ContactService()

    contact = create_contact(
        service,
        db_session,
    )

    found = service.get(
        db_session,
        contact.id,
    )

    assert found is not None

    assert found.id == contact.id


# ==========================================================
# Update
# ==========================================================


def test_update(
    db_session,
):

    service = ContactService()

    contact = create_contact(
        service,
        db_session,
    )

    updated = service.update(
        db_session,
        contact,
        ContactUpdate(
            job_title="CEO",
        ),
    )

    assert updated.job_title == "CEO"


# ==========================================================
# Exists
# ==========================================================


def test_exists(
    db_session,
):

    service = ContactService()

    create_contact(
        service,
        db_session,
    )

    assert service.exists(
        db_session,
        "john@example.com",
    )

    assert not service.exists(
        db_session,
        "missing@test.com",
    )


# ==========================================================
# Find By Email
# ==========================================================


def test_find_by_email(
    db_session,
):

    service = ContactService()

    create_contact(
        service,
        db_session,
    )

    contact = service.find_by_email(
        db_session,
        "john@example.com",
    )

    assert contact is not None

    assert contact.email == "john@example.com"


# ==========================================================
# List By Lead
# ==========================================================


def test_list_by_lead(
    db_session,
):

    service = ContactService()

    create_contact(
        service,
        db_session,
        email="a@test.com",
    )

    create_contact(
        service,
        db_session,
        email="b@test.com",
    )

    contacts = service.list_by_lead(
        db_session,
        1,
    )

    assert len(
        contacts,
    ) == 2


# ==========================================================
# Primary Contact
# ==========================================================


def test_primary_contact(
    db_session,
):

    service = ContactService()

    create_contact(
        service,
        db_session,
        email="a@test.com",
    )

    second = create_contact(
        service,
        db_session,
        email="b@test.com",
    )

    service.set_primary(
        db_session,
        second,
    )

    primary = service.get_primary(
        db_session,
        1,
    )

    assert primary is not None

    assert primary.email == "b@test.com"


# ==========================================================
# Delete
# ==========================================================


def test_delete(
    db_session,
):

    service = ContactService()

    contact = create_contact(
        service,
        db_session,
    )

    service.delete(
        db_session,
        contact,
    )

    assert (
        service.get(
            db_session,
            contact.id,
        )
        is None
    )