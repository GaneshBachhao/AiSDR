"""
Base payload for all automation actions.
"""

from pydantic import BaseModel
from pydantic import ConfigDict


class BaseAutomationPayload(BaseModel):
    """
    Base class for every automation payload.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )