"""
AI Mapper

Maps between Application DTOs and Domain objects.
"""

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)
from app.application.ai.dto.ai_request_dto import (
    AIRequestDTO,
)
from app.application.ai.dto.ai_response_dto import (
    AIResponseDTO,
    TokenUsageDTO,
)
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature


class AIMapper:
    """
    Mapper for AI application layer.
    """

    @staticmethod
    def command_to_dto(
        command: ExecuteAIRequestCommand,
    ) -> AIRequestDTO:

        return AIRequestDTO(
            provider=command.provider,
            model=command.model,
            prompt=command.prompt,
            temperature=command.temperature,
            max_tokens=command.max_tokens,
        )

    @staticmethod
    def dto_to_domain(
        dto: AIRequestDTO,
    ) -> AIRequest:

        return AIRequest(
            provider=ProviderName(dto.provider),
            model=ModelName(dto.model),
            prompt=Prompt(dto.prompt),
            temperature=Temperature(dto.temperature),
            max_tokens=MaxTokens(dto.max_tokens),
        )

    @staticmethod
    def response_to_dto(
        response: AIResponse,
    ) -> AIResponseDTO:

        return AIResponseDTO(
            response_id=str(response.id),
            content=response.content,
            finish_reason=response.finish_reason.value,
            token_usage=TokenUsageDTO(
                prompt_tokens=response.token_usage.prompt_tokens,
                completion_tokens=response.token_usage.completion_tokens,
                total_tokens=response.token_usage.total_tokens,
            ),
            created_at=response.created_at,
        )