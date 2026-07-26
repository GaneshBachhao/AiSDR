from fastapi import APIRouter

from .health_router import router as health_router
from .lead_router import router as lead_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(lead_router)