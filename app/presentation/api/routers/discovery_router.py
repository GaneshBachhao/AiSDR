from fastapi import APIRouter, status

from app.application.discovery.commands.start_discovery.start_discovery_command import (
    StartDiscoveryCommand,
)
from app.application.common.interfaces.mediator import Mediator
from app.presentation.api.dependencies.mediator import MediatorDependency
from app.presentation.common.response import ApiResponse
from app.presentation.schemas.requests.discovery_request import (
    StartDiscoveryRequest,
)
from app.presentation.schemas.responses.discovery_response import (
    DiscoveryResponse,
)

router = APIRouter(
    prefix="/discoveries",
    tags=["Discovery"],
)


@router.post(
    "",
    response_model=ApiResponse[DiscoveryResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_discovery(
    request: StartDiscoveryRequest,
    mediator: MediatorDependency,
) -> ApiResponse[DiscoveryResponse]:

    command = StartDiscoveryCommand(
        company_name=request.company_name,
        website=request.website,
    )

    result = await mediator.send(command)

    return ApiResponse(
        success=True,
        message="Discovery started successfully.",
        data=DiscoveryResponse.model_validate(result),
    )