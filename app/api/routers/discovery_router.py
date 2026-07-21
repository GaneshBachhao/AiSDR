"""
Discovery Router

Endpoints for discovering companies.
"""

from fastapi import APIRouter, HTTPException, status

from app.discovery.schemas.discovery_schema import (
    DiscoveryRequest,
)

from app.discovery.services.discovery_service import (
    DiscoveryService,
)

discovery_router = APIRouter(

    prefix="/discover",

    tags=["Discovery"],

)

service = DiscoveryService()


# ==========================================================
# Discover Companies
# ==========================================================

@discovery_router.post(
    "",
    summary="Discover Companies",
)
def discover(
    request: DiscoveryRequest,
):
    """
    Discover companies matching the supplied criteria.
    """

    try:

        results = service.discover(
            request
        )

        return {

            "success": True,

            "count": len(results),

            "results": results,

        }

    except Exception as ex:

        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=str(ex),

        ) from ex