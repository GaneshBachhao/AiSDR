# app/domain/workflow/identifiers/workflow_id.py

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class WorkflowId:
    """
    Strongly typed identifier for Workflow aggregates.
    """

    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)