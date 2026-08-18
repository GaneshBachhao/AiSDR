"""
AI Request repository contract.
"""

from __future__ import annotations

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.ai.aggregates.ai_request import (
    AIRequest,
)
from app.domain.ai.value_objects.ai_request_id import (
    AIRequestId,
)


class AIRequestRepository(
    Repository[
        AIRequest,
        AIRequestId,
    ],
):
    """
    Contract for AIRequest persistence.

    Generic CRUD operations are inherited from Repository.
    Additional AI-specific queries can be added here as needed.
    """

    # No AI-specific queries yet.
    # Add them here when required.
    pass
