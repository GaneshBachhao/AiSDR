from typing import List

from pydantic import BaseModel


class RecommendationItem(BaseModel):
    """
    Represents a single AI solution recommendation.
    """

    service_id: str

    service_name: str

    category: str

    priority: str

    difficulty: str

    roi: str

    target_personas: List[str]

    deliverables: List[str]

    estimated_duration_weeks: int


class RecommendationResponse(BaseModel):
    """
    Recommendation result returned by RecommendationService.
    """

    matched_sector: str

    sector_confidence: float

    recommendations: List[RecommendationItem]

    generic_ai_opportunities: List[str]