"""
Tests for ContactRepository.
"""

from app.contacts.repositories.contact_repository import (
    ContactRepository,
)

from app.contacts.schemas.contact_schema import (
    ContactCreate,
    ContactUpdate,
)


def create_contact(
    repo,
    db_session,
    email="john@example.com",
    lead_id=1,
    primary=False,
):

    return repo.create(
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


def test_create_contact(
    db_session,
):

    repo = ContactRepository()

    contact = create_contact(
        repo,
        db_session,
    )

    assert contact.id is not None

    assert contact.email == "john@example.com"

    assert contact.full_name == "John Doe"


# ==========================================================
# Get By ID
# ==========================================================


def test_get_by_id(
    db_session,
):

    repo = ContactRepository()

    created = create_contact(
        repo,
        db_session,
    )

    found = repo.get_by_id(
        db_session,
        created.id,
    )

    assert found is not None

    assert found.id == created.id


# ==========================================================
# Find By Email
# ==========================================================


def test_find_by_email(
    db_session,
):

    repo = ContactRepository()

    create_contact(
        repo,
        db_session,
    )

    contact = repo.find_by_email(
        db_session,
        "john@example.com",
    )

    assert contact is not None

    assert contact.email == "john@example.com"


# ==========================================================
# Exists
# ==========================================================


def test_exists(
    db_session,
):

    repo = ContactRepository()

    create_contact(
        repo,
        db_session,
    )

    assert repo.exists(
        db_session,
        "john@example.com",
    )

    assert not repo.exists(
        db_session,
        "missing@example.com",
    )


# ==========================================================
# List By Lead
# ==========================================================


def test_list_by_lead(
    db_session,
):

    repo = ContactRepository()

    create_contact(
        repo,
        db_session,
        email="a@test.com",
    )

    create_contact(
        repo,
        db_session,
        email="b@test.com",
    )

    contacts = repo.list_by_lead(
        db_session,
        1,
    )

    assert len(
        contacts,
    ) == 2


# ==========================================================
# Update
# ==========================================================


def test_update_contact(
    db_session,
):

    repo = ContactRepository()

    contact = create_contact(
        repo,
        db_session,
    )

    updated = repo.update(
        db_session,
        contact,
        ContactUpdate(
            job_title="CEO",
        ),
    )

    assert updated.job_title == "CEO"


# ==========================================================
# Delete
# ==========================================================


def test_delete_contact(
    db_session,
):

    repo = ContactRepository()

    contact = create_contact(
        repo,
        db_session,
    )

    repo.delete(
        db_session,
        contact,
    )

    deleted = repo.get_by_id(
        db_session,
        contact.id,
    )

    assert deleted is None


# ==========================================================
# Primary Contact
# ==========================================================


def test_set_primary(
    db_session,
):

    repo = ContactRepository()

    contact1 = create_contact(
        repo,
        db_session,
        email="a@test.com",
    )

    contact2 = create_contact(
        repo,
        db_session,
        email="b@test.com",
    )

    repo.set_primary(
        db_session,
        contact2,
    )

    primary = repo.get_primary_contact(
        db_session,
        1,
    )

    assert primary is not None

    assert primary.email == "b@test.com"

    assert primary.is_primary


# ==========================================================
# No Primary
# ==========================================================


def test_get_primary_none(
    db_session,
):

    repo = ContactRepository()

    create_contact(
        repo,
        db_session,
    )

    assert (
        repo.get_primary_contact(
            db_session,
            1,
        )
        is None
    )