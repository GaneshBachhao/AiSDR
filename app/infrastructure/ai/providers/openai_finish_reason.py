"""
Shared finish-reason mapping for the OpenAI-compatible chat completions API.

Azure OpenAI uses the same finish-reason vocabulary as OpenAI, so both
providers map through this one table.
"""

from __future__ import annotations

from app.domain.ai.enums.finish_reason import FinishReason

_OPENAI_FINISH_REASON_MAP = {
    "stop": FinishReason.STOP,
    "length": FinishReason.LENGTH,
    "tool_calls": FinishReason.TOOL_CALL,
    "function_call": FinishReason.TOOL_CALL,
    "content_filter": FinishReason.CONTENT_FILTER,
}


def map_openai_finish_reason(raw: str) -> FinishReason:
    return _OPENAI_FINISH_REASON_MAP.get(raw.lower(), FinishReason.STOP)
