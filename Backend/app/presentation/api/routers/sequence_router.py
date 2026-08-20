"""
Sequence API router (EPIC-09.1).

Internal CRM/ops action -- gated behind the blanket auth gate like every
other router, same tier as outcome_router/suppression_router.
"""

from __future__ import annotations

from fastapi import APIRouter, Query, status

from app.application.sequence.dto.sequence_requests import CreateSequenceRequestDTO
from app.application.sequence.dto.sequence_responses import SequenceResponseDTO
from app.application.sequence.sequence_commands import (
    AdvanceSequenceCommand,
    RecordSequenceBounceCommand,
    RecordSequenceReplyCommand,
    StartSequenceCommand,
)
from app.application.sequence.sequence_mapper import SequenceMapper
from app.presentation.api.dependencies.handlers import (
    AdvanceSequenceHandlerDependency,
    CreateSequenceHandlerDependency,
    GetSequenceHandlerDependency,
    ListSequencesHandlerDependency,
    RecordSequenceBounceHandlerDependency,
    RecordSequenceReplyHandlerDependency,
    StartSequenceHandlerDependency,
)

router = APIRouter(
    prefix="/sequences",
    tags=["Sequences"],
)


@router.post(
    "",
    response_model=SequenceResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_sequence(
    request: CreateSequenceRequestDTO,
    handler: CreateSequenceHandlerDependency,
) -> SequenceResponseDTO:
    """Create a planned touch cadence for a Lead."""
    return await handler.handle(SequenceMapper.to_create_command(request))


@router.get(
    "",
    response_model=list[SequenceResponseDTO],
)
async def list_sequences(
    handler: ListSequencesHandlerDependency,
    lead_id: str = Query(...),
) -> list[SequenceResponseDTO]:
    """List Sequences for one Lead."""
    return await handler.handle(lead_id)


@router.get(
    "/{sequence_id}",
    response_model=SequenceResponseDTO,
)
async def get_sequence(
    sequence_id: str,
    handler: GetSequenceHandlerDependency,
) -> SequenceResponseDTO:
    """Get a Sequence by ID."""
    return await handler.handle(sequence_id)


@router.post(
    "/{sequence_id}/start",
    response_model=SequenceResponseDTO,
)
async def start_sequence(
    sequence_id: str,
    handler: StartSequenceHandlerDependency,
) -> SequenceResponseDTO:
    """Begin a Sequence's touch cadence. Requires the Lead to be Approved."""
    return await handler.handle(StartSequenceCommand(sequence_id=sequence_id))


@router.post(
    "/{sequence_id}/advance",
    response_model=SequenceResponseDTO,
)
async def advance_sequence(
    sequence_id: str,
    handler: AdvanceSequenceHandlerDependency,
) -> SequenceResponseDTO:
    """Mark the current touch as sent and move to the next one."""
    return await handler.handle(AdvanceSequenceCommand(sequence_id=sequence_id))


@router.post(
    "/{sequence_id}/reply",
    response_model=SequenceResponseDTO,
)
async def record_sequence_reply(
    sequence_id: str,
    handler: RecordSequenceReplyHandlerDependency,
) -> SequenceResponseDTO:
    """Stop a Sequence early: the Lead replied."""
    return await handler.handle(RecordSequenceReplyCommand(sequence_id=sequence_id))


@router.post(
    "/{sequence_id}/bounce",
    response_model=SequenceResponseDTO,
)
async def record_sequence_bounce(
    sequence_id: str,
    handler: RecordSequenceBounceHandlerDependency,
) -> SequenceResponseDTO:
    """Stop a Sequence early: a touch bounced."""
    return await handler.handle(RecordSequenceBounceCommand(sequence_id=sequence_id))
