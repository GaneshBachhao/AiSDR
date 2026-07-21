"""
Insight Schema

Represents business intelligence generated
from enterprise reasoning.
"""

from pydantic import BaseModel


class Insight(BaseModel):
    """
    Business insight.
    """

    category: str

    title: str

    description: str

    confidence: float

    recommendation: str