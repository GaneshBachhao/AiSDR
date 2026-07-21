"""
Conversation Repository Tests
"""

from app.conversations.enums.conversation_status import (
    ConversationStatus,
)

from app.conversations.repositories.conversation_repository import (
    ConversationRepository,
)

from app.conversations.schemas.conversation_schema import (
    ConversationCreate,
    ConversationUpdate,
)


# ==========================================================
# Helpers
# ==========================================================


def create_conversation(
    repo: ConversationRepository,
    db_session,
):
    """
    Create a test conversation.
    """

    return repo.create(
        db_session,
        ConversationCreate(
            lead_id=1,
            contact_id=1,
            provider="gmail",
            provider_thread_id="thread123",
        ),
    )


# ==========================================================
# Create
# ==========================================================


def test_create_conversation(
    db_session,
):

    repo = ConversationRepository()

    conversation = create_conversation(
        repo,
        db_session,
    )

    assert conversation.id is not None

    assert conversation.provider == "gmail"

    assert conversation.provider_thread_id == "thread123"

    assert conversation.status == ConversationStatus.OPEN


# ==========================================================
# Get By ID
# ==========================================================


def test_get_by_id(
    db_session,
):

    repo = ConversationRepository()

    conversation = create_conversation(
        repo,
        db_session,
    )

    loaded = repo.get_by_id(
        db_session,
        conversation.id,
    )

    assert loaded is not None

    assert loaded.id == conversation.id


# ==========================================================
# Find By Thread
# ==========================================================


def test_find_by_provider_thread(
    db_session,
):

    repo = ConversationRepository()

    create_conversation(
        repo,
        db_session,
    )

    conversation = repo.find_by_provider_thread(
        db_session,
        "thread123",
    )

    assert conversation is not None

    assert conversation.provider_thread_id == "thread123"


# ==========================================================
# Exists
# ==========================================================


def test_exists(
    db_session,
):

    repo = ConversationRepository()

    create_conversation(
        repo,
        db_session,
    )

    assert repo.exists(
        db_session,
        "thread123",
    ) is True

    assert repo.exists(
        db_session,
        "unknown-thread",
    ) is False


# ==========================================================
# List By Lead
# ==========================================================


def test_list_by_lead(
    db_session,
):

    repo = ConversationRepository()

    create_conversation(
        repo,
        db_session,
    )

    conversations = repo.list_by_lead(
        db_session,
        1,
    )

    assert len(conversations) == 1

    assert conversations[0].lead_id == 1


# ==========================================================
# List Open
# ==========================================================


def test_list_open(
    db_session,
):

    repo = ConversationRepository()

    create_conversation(
        repo,
        db_session,
    )

    conversations = repo.list_open(
        db_session,
    )

    assert len(conversations) == 1

    assert conversations[0].status == ConversationStatus.OPEN


# ==========================================================
# Update
# ==========================================================


def test_update(
    db_session,
):

    repo = ConversationRepository()

    conversation = create_conversation(
        repo,
        db_session,
    )

    updated = repo.update(
        db_session,
        conversation,
        ConversationUpdate(
            status=ConversationStatus.RESPONDED,
        ),
    )

    assert updated.status == ConversationStatus.RESPONDED


# ==========================================================
# Delete
# ==========================================================


def test_delete(
    db_session,
):

    repo = ConversationRepository()

    conversation = create_conversation(
        repo,
        db_session,
    )

    repo.delete(
        db_session,
        conversation,
    )

    loaded = repo.get_by_id(
        db_session,
        conversation.id,
    )

    assert loaded is None