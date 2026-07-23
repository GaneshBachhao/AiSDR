"""
Mapper between AIRequest aggregate and AIRequestModel.
"""

from __future__ import annotations

from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.ai_request_status import AIRequestStatus
from app.domain.ai.enums.finish_reason import FinishReason
from app.domain.ai.value_objects.ai_request_id import AIRequestId
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.response_id import ResponseId
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.ai.value_objects.token_usage import TokenUsage

from app.infrastructure.persistence.models.ai_request_model import (
    AIRequestModel,
)


class AIRequestMapper:
    """
    Maps AIRequest aggregate to persistence model
    and vice versa.
    """

    @staticmethod
    def to_model(
        request: AIRequest,
    ) -> AIRequestModel:
        """
        Convert domain aggregate to ORM model.
        """

        return AIRequestModel(
            id=str(request.id),
            provider=request.provider.value,
            model=request.model.value,
            prompt=request.prompt.value,
            temperature=request.temperature.value,
            max_tokens=request.max_tokens.value,
            status=request.status.value,
            response=(
                request.response.content
                if request.response
                else None
            ),
            failure_reason=request.failure_reason,
            started_at=request.started_at,
            completed_at=request.completed_at,
            created_at=request.created_at,
            updated_at=request.updated_at,
        )

    @staticmethod
    def to_domain(
        model: AIRequestModel,
    ) -> AIRequest:
        """
        Convert ORM model to domain aggregate.
        """

        response = None

        if model.response:

            response = AIResponse(
                id=ResponseId(),
                content=model.response,
                finish_reason=FinishReason.STOP,
                token_usage=TokenUsage(),
            )

        request = AIRequest(
            id=AIRequestId(model.id),
            provider=ProviderName(model.provider),
            model=ModelName(model.model),
            prompt=Prompt(model.prompt),
            temperature=Temperature(model.temperature),
            max_tokens=MaxTokens(model.max_tokens),
            status=AIRequestStatus(model.status),
            response=response,
            failure_reason=model.failure_reason,
            started_at=model.started_at,
            completed_at=model.completed_at,
        )

        request.created_at = model.created_at
        request.updated_at = model.updated_at

        return request