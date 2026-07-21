"""
AI Domain Module.

Responsible for modeling AI interactions,
requests, responses, and execution lifecycle.
"""

from .aggregate import AIRequest

from .entities import (
    AIMessage,
    AIResponse,
)

from .value_objects import (
    AIRequestId,
    MessageId,
    ResponseId,
    ProviderName,
    ModelName,
    Temperature,
    MaxTokens,
    TokenUsage,
)

from .enums import (
    AIRequestStatus,
    MessageRole,
    FinishReason,
)

__all__ = [
    "AIRequest",

    "AIMessage",
    "AIResponse",

    "AIRequestId",
    "MessageId",
    "ResponseId",
    "ProviderName",
    "ModelName",
    "Temperature",
    "MaxTokens",
    "TokenUsage",

    "AIRequestStatus",
    "MessageRole",
    "FinishReason",
]