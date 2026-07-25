"""
Lead repository contract.
"""

from __future__ import annotations

from app.application.common.interfaces.repository import (
    Repository,
)
from app.domain.lead.entities.lead import Lead
from app.domain.lead.identifiers.lead_id import LeadId


class LeadRepository(
    Repository[Lead, LeadId],
):
    """
    Lead persistence contract.
    """

    pass