"""
Sequence persistence mapper.

Touch channel/wait_days/position are set once at creation and never
mutated afterward; the touches list itself never changes shape (count/
order), so update_model() never rebuilds the touches relationship --
avoiding delete-orphan diffing entirely. Touch.content (EPIC-09.2) is the
one field that *does* get updated post-creation: since the list is
positionally stable, update_model() zips the existing (already-loaded)
model touches against the entity's touches and copies content across,
which is a plain scalar update on already-persisted child rows, not a
collection-shape change.
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
                Touch(
                    channel=TouchChannel(touch.channel),
                    wait_days=touch.wait_days,
                    content=touch.content,
                )
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
                    content=touch.content,
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

        # Touches never change count/order after creation -- model.touches
        # (already loaded via lazy="selectin", ordered by position) and
        # entity.touches are always the same length, in the same order.
        # Only content can differ; everything else is asserted unchanged
        # by the domain layer itself (Touch's other fields are set once).
        for model_touch, entity_touch in zip(model.touches, entity.touches, strict=True):
            model_touch.content = entity_touch.content

        return model
