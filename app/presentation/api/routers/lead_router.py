"""
Lead API routes.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import status

from app.application.lead.commands.create_lead import (
    CreateLeadCommand,
)
from app.presentation.api.dependencies.handlers import (
    CreateLeadHandlerDependency,
)
from app.presentation.common.response import (
    ApiResponse,
)
from app.presentation.schemas.requests.lead_request import (
    CreateLeadRequest,
)
from app.presentation.schemas.responses.lead_response import (
    LeadResponse,
)

router = APIRouter(
    prefix="/leads",
    tags=["Leads"],
)


@router.post(
    "",
    response_model=ApiResponse[LeadResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_lead(
    request: CreateLeadRequest,
    handler: CreateLeadHandlerDependency,
) -> ApiResponse[LeadResponse]:
    """
    Create a new lead.
    """

    command = CreateLeadCommand(
        company_name=request.company_name,
        contact_name=request.contact_name,
        email=request.email,
        phone=request.phone,
        website=request.website,
    )

    lead = await handler.handle(command)

    return ApiResponse(
        success=True,
        message="Lead created successfully.",
        data=LeadResponse.model_validate(
            lead,
        ),
    )