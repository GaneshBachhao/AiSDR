"""
AI Request repository contract.
"""

from __future__ import annotations

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.ai.entities.ai_request import (
    AIRequest,
)
from app.domain.ai.identifiers.request_id import (
    RequestId,
)


class AIRequestRepository(
    Repository[
        AIRequest,
        RequestId,
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