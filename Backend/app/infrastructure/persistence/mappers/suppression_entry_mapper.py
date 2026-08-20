"""
SuppressionEntry persistence mapper.

SuppressionEntry is create-only (no update use case -- an entry is either
added or lifted/deleted), so there's no update_model() here the way
Lead/Recommendation/User have -- there's nothing that would ever call it.
"""

from __future__ import annotations

from app.domain.contact.value_objects.email import Email
from app.domain.suppression.entities.suppression_entry import SuppressionEntry
from app.domain.suppression.enums.suppression_reason import SuppressionReason
from app.domain.suppression.identifiers.suppression_entry_id import SuppressionEntryId
from app.infrastructure.persistence.models.suppression_entry_model import SuppressionEntryModel


class SuppressionEntryMapper:
    """Maps SuppressionEntry domain entities and ORM models."""

    @staticmethod
    def to_domain(model: SuppressionEntryModel) -> SuppressionEntry:
        entry = SuppressionEntry(
            id=SuppressionEntryId(model.id),
            email=Email(model.email),
            reason=SuppressionReason(model.reason),
            notes=model.notes,
            suppressed_at=model.suppressed_at,
        )
        entry.created_at = model.created_at
        entry.updated_at = model.updated_at
        return entry

    @staticmethod
    def to_model(entity: SuppressionEntry) -> SuppressionEntryModel:
        return SuppressionEntryModel(
            id=entity.id.value,
            email=entity.email.value,
            reason=entity.reason.value,
            notes=entity.notes,
            suppressed_at=entity.suppressed_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
