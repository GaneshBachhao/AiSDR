"""
LLM Response

Represents a normalized response returned
by any Large Language Model provider.
"""

from pydantic import BaseModel


class LLMResponse(BaseModel):
    """
    Standard response from an LLM.
    """

    # ---------------------------------------------------------
    # Generated Content
    # ---------------------------------------------------------

    text: str

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    model: str

    provider: str

    # ---------------------------------------------------------
    # Usage
    # ---------------------------------------------------------

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    finish_reason: str | None = None

    latency_ms: float | None = None