from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.discovery.agents.discovery_agent import DiscoveryAgent
from app.discovery.schemas.discovery_schema import DiscoveryRequest
from app.common.response import ApiResponse

router = APIRouter(
    prefix="/api/v1/discovery",
    tags=["Discovery"]
)

agent = DiscoveryAgent()


@router.post("/run")
def run_discovery(
    request: DiscoveryRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    background_tasks.add_task(
        agent.execute_async,
        request
    )

    return ApiResponse.success(
        message="Discovery started successfully."
    )