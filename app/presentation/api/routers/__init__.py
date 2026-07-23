from fastapi import APIRouter

from .ai_router import router as ai_router
from .assessment_router import router as assessment_router
from .discovery_router import router as discovery_router
from .health_router import router as health_router
from .lead_router import router as lead_router
from .recommendation_router import router as recommendation_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(ai_router)
api_router.include_router(lead_router)
api_router.include_router(discovery_router)
api_router.include_router(assessment_router)
api_router.include_router(recommendation_router)