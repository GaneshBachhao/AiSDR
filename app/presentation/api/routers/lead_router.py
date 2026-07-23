from fastapi import APIRouter, status

from app.application.lead.commands.create_lead.create_lead_command import (
    CreateLeadCommand,
)
from app.application.lead.handlers.create_lead_handler import (
    CreateLeadHandler,
)
from app.presentation.api.dependencies.persistence import (
    UnitOfWorkDependency,
)
from app.presentation.common.response import ApiResponse
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
    unit_of_work: UnitOfWorkDependency,
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
        notes=request.notes,
    )

    handler = CreateLeadHandler(unit_of_work)

    lead = await handler.handle(command)

    return ApiResponse(
        success=True,
        message="Lead created successfully.",
        data=LeadResponse.model_validate(lead),
    )