"""
Discovery Request DTO

DTO used internally by the Application layer.
"""

from pydantic import BaseModel, ConfigDict


class DiscoveryRequestDTO(BaseModel):
    """
    Internal DTO for company discovery.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    industry: str

    location: str

    max_results: int = 10