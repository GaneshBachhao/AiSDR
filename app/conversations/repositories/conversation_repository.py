"""
Conversation Repository

Persistence layer for Conversation.
"""

from sqlalchemy.orm import Session

from app.conversations.schemas.conversation_schema import (
    ConversationCreate,
    ConversationUpdate,
)

from app.conversations.enums.conversation_status import (
    ConversationStatus,
)

from app.models.conversation import Conversation


class ConversationRepository:
    """
    Repository for Conversation persistence.
    """

    # ======================================================
    # Create
    # ======================================================

    def create(
        self,
        db: Session,
        conversation: ConversationCreate,
    ) -> Conversation:

        db_conversation = Conversation(
            **conversation.model_dump()
        )

        db.add(
            db_conversation,
        )

        db.commit()

        db.refresh(
            db_conversation,
        )

        return db_conversation

    # ======================================================
    # Update
    # ======================================================

    def update(
        self,
        db: Session,
        conversation: Conversation,
        update: ConversationUpdate,
    ) -> Conversation:

        values = update.model_dump(
            exclude_unset=True,
        )

        for key, value in values.items():

            setattr(
                conversation,
                key,
                value,
            )

        db.commit()

        db.refresh(
            conversation,
        )

        return conversation

    # ======================================================
    # Delete
    # ======================================================

    def delete(
        self,
        db: Session,
        conversation: Conversation,
    ) -> None:

        db.delete(
            conversation,
        )

        db.commit()

    # ======================================================
    # Queries
    # ======================================================

    def get_by_id(
        self,
        db: Session,
        conversation_id: int,
    ) -> Conversation | None:

        return (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
            )
            .first()
        )

    def find_by_provider_thread(
        self,
        db: Session,
        provider_thread_id: str,
    ) -> Conversation | None:

        return (
            db.query(Conversation)
            .filter(
                Conversation.provider_thread_id
                == provider_thread_id
            )
            .first()
        )

    def list_by_lead(
        self,
        db: Session,
        lead_id: int,
    ) -> list[Conversation]:

        return (
            db.query(Conversation)
            .filter(
                Conversation.lead_id == lead_id,
            )
            .all()
        )

    def list_open(
        self,
        db: Session,
    ) -> list[Conversation]:

        return (
            db.query(Conversation)
            .filter(
                Conversation.status != ConversationStatus.CLOSED,
            )
            .all()
        )

    def exists(
        self,
        db: Session,
        provider_thread_id: str,
    ) -> bool:

        return (

            self.find_by_provider_thread(

                db,

                provider_thread_id,

            )

            is not None

        )