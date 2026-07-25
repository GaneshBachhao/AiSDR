"""
AI related application DTOs.

These models represent AI communication data exchanged between
application use cases and AI provider ports.
"""

from app.application.common.dto.response_dto import ResponseDTO


class AICompletionResponse(ResponseDTO):
    """
    Standard AI completion response.
    """

    content: str

    model: str

    input_tokens: int = 0

    output_tokens: int = 0