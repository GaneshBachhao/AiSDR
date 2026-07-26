"""
Application handler dependencies.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.application.lead.handlers.create_lead_handler import (
    CreateLeadHandler,
)
from app.application.lead.mappers.lead_mapper import (
    LeadMapper,
)
from app.application.lead.validators.create_lead_validator import (
    CreateLeadValidator,
)
from app.presentation.api.dependencies.persistence import (
    UnitOfWorkDependency,
)


def get_create_lead_handler(
    unit_of_work: UnitOfWorkDependency,
) -> CreateLeadHandler:
    """
    Resolve CreateLeadHandler.
    """

    return CreateLeadHandler(
        repository=unit_of_work.leads,
        validator=CreateLeadValidator(),
        mapper=LeadMapper(),
    )


CreateLeadHandlerDependency = Annotated[
    CreateLeadHandler,
    Depends(get_create_lead_handler),
]