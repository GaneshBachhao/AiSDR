from fastapi import APIRouter

from .admin_router import router as admin_router
from .company_router import router as company_router
from .company_research_router import router as company_research_router
from .discovery_router import router as discovery_router
from .health_router import router as health_router
from .lead_router import router as lead_router
from .contact_router import router as contact_router
from .assessment_router import router as assessment_router
from .qualification_router import router as qualification_router
from .recommendation_router import router as recommendation_router


api_router = APIRouter()


api_router.include_router(admin_router)
api_router.include_router(health_router)
api_router.include_router(company_router)
api_router.include_router(company_research_router)
api_router.include_router(discovery_router)
api_router.include_router(lead_router)
api_router.include_router(contact_router)
api_router.include_router(assessment_router)
api_router.include_router(qualification_router)
api_router.include_router(recommendation_router)
