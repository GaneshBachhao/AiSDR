"""
Sequence application commands.

Commands represent write operations on the Sequence aggregate.
"""

from __future__ import annotations

from app.application.common.commands.command import Command
from app.application.common.dto.request_dto import RequestDTO
from app.domain.sequence.enums.touch_channel import TouchChannel


class TouchInput(RequestDTO):
    """One planned touch, as supplied when creating a Sequence."""

    channel: TouchChannel
    wait_days: int


class CreateSequenceCommand(Command):
    """Command to create a Sequence for a Lead."""

    lead_id: str
    touches: list[TouchInput]


class StartSequenceCommand(Command):
    """Command to begin a Sequence's touch cadence."""

    sequence_id: str


class AdvanceSequenceCommand(Command):
    """Command to mark the current touch as sent and move to the next one."""

    sequence_id: str


class RecordSequenceReplyCommand(Command):
    """Command to stop a Sequence early: the Lead replied."""

    sequence_id: str


class RecordSequenceBounceCommand(Command):
    """Command to stop a Sequence early: a touch bounced."""

    sequence_id: str


class GenerateSequenceContentCommand(Command):
    """Command to AI-generate content for every touch in a Sequence."""

    sequence_id: str
