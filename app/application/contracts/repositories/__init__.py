"""
Application repository contracts.
"""

from .assessment_repository import AssessmentRepository
from .discovery_repository import DiscoveryRepository
from .lead_repository import LeadRepository
from .recommendation_repository import RecommendationRepository


__all__ = [
    "AssessmentRepository",
    "DiscoveryRepository",
    "LeadRepository",
    "RecommendationRepository",
]