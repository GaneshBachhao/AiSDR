from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddSolutionCommand:

    recommendation_id: UUID

    title: str

    description: str

    solution_type: str

    priority: str