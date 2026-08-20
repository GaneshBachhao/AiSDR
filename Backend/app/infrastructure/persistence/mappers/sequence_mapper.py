"""
Sequence persistence mapper.

Touches are set once at creation and never mutated afterward, so
update_model() only ever touches Sequence's own scalar fields -- it never
rebuilds the touches relationship, avoiding delete-orphan diffing for
something that's immutable by design.
"""

from __future__ import annotations

from app.domain.lead.identifiers.lead_id import LeadId
from app.domain.sequence.entities.sequence import Sequence
from app.domain.sequence.enums.sequence_status import SequenceStatus
from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.identifiers.sequence_id import SequenceId
from app.domain.sequence.value_objects.touch import Touch
from app.infrastructure.persistence.models.sequence_model import SequenceModel
from app.infrastructure.persistence.models.sequence_touch_model import SequenceTouchModel


class SequenceMapper:
    """Maps Sequence domain entities and ORM models."""

    @staticmethod
    def to_domain(model: SequenceModel) -> Sequence:
        sequence = Sequence(
            id=SequenceId(model.id),
            lead_id=LeadId(model.lead_id),
            touches=[
                Touch(channel=TouchChannel(touch.channel), wait_days=touch.wait_days)
                for touch in model.touches
            ],
            status=SequenceStatus(model.status),
            current_touch_index=model.current_touch_index,
            started_at=model.started_at,
            ended_at=model.ended_at,
            stop_reason=model.stop_reason,
        )
        sequence.created_at = model.created_at
        sequence.updated_at = model.updated_at
        return sequence

    @staticmethod
    def to_model(entity: Sequence) -> SequenceModel:
        return SequenceModel(
            id=entity.id.value,
            lead_id=entity.lead_id.value,
            status=entity.status.value,
            current_touch_index=entity.current_touch_index,
            started_at=entity.started_at,
            ended_at=entity.ended_at,
            stop_reason=entity.stop_reason,
            touches=[
                SequenceTouchModel(
                    position=position,
                    channel=touch.channel.value,
                    wait_days=touch.wait_days,
                )
                for position, touch in enumerate(entity.touches)
            ],
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: SequenceModel, entity: Sequence) -> SequenceModel:
        model.status = entity.status.value
        model.current_touch_index = entity.current_touch_index
        model.started_at = entity.started_at
        model.ended_at = entity.ended_at
        model.stop_reason = entity.stop_reason
        return model
