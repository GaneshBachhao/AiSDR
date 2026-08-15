"""
Tests for AIMapper.
"""

from app.application.ai.commands.execute_ai_request import (
    ExecuteAIRequestCommand,
)
from app.application.ai.dto.ai_request_dto import (
    AIRequestDTO,
)
from app.application.ai.dto.ai_response_dto import (
    AIResponseDTO,
)
from app.application.ai.mappers.ai_mapper import (
    AIMapper,
)
from app.domain.ai.entities.ai_response import (
    AIResponse,
)
from app.domain.ai.enums.finish_reason import (
    FinishReason,
)
from app.domain.ai.value_objects.token_usage import (
    TokenUsage,
)
from app.domain.ai.aggregates.ai_request import (
    AIRequest,
)


# ==========================================================
# Helpers
# ==========================================================

def create_command() -> ExecuteAIRequestCommand:
    return ExecuteAIRequestCommand(
        provider="gemini",
        model="gemini-2.5-pro",
        prompt="Explain Clean Architecture",
        temperature=0.8,
        max_tokens=2048,
    )


def create_response() -> AIResponse:
    return AIResponse(
        content="Architecture explained.",
        finish_reason=FinishReason.STOP,
        token_usage=TokenUsage(
            prompt_tokens=20,
            completion_tokens=80,
        ),
    )


# ==========================================================
# Command -> DTO
# ==========================================================

def test_command_to_dto():
    command = create_command()

    dto = AIMapper.command_to_dto(command)

    assert isinstance(dto, AIRequestDTO)

    assert dto.provider == command.provider
    assert dto.model == command.model
    assert dto.prompt == command.prompt
    assert dto.temperature == command.temperature
    assert dto.max_tokens == command.max_tokens


# ==========================================================
# DTO -> Domain
# ==========================================================

def test_dto_to_domain():
    dto = AIRequestDTO(
        provider="gemini",
        model="gemini-2.5-pro",
        prompt="Hello",
        temperature=0.7,
        max_tokens=1024,
    )

    request = AIMapper.dto_to_domain(dto)

    assert isinstance(request, AIRequest)

    assert request.provider.value == dto.provider
    assert request.model.value == dto.model
    assert request.prompt.value == dto.prompt
    assert request.temperature.value == dto.temperature
    assert request.max_tokens.value == dto.max_tokens


# ==========================================================
# Response -> DTO
# ==========================================================

def test_response_to_dto():
    response = create_response()

    dto = AIMapper.response_to_dto(response)

    assert isinstance(dto, AIResponseDTO)

    assert dto.response_id == str(response.id)
    assert dto.content == response.content
    assert dto.finish_reason == response.finish_reason.value


# ==========================================================
# Token Usage Mapping
# ==========================================================

def test_token_usage_mapping():
    response = create_response()

    dto = AIMapper.response_to_dto(response)

    assert dto.token_usage.prompt_tokens == 20
    assert dto.token_usage.completion_tokens == 80
    assert dto.token_usage.total_tokens == 100


# ==========================================================
# Finish Reason Mapping
# ==========================================================

def test_finish_reason_mapping():
    response = create_response()

    dto = AIMapper.response_to_dto(response)

    assert dto.finish_reason == FinishReason.STOP.value


# ==========================================================
# Timestamp Mapping
# ==========================================================

def test_created_at_mapping():
    response = create_response()

    dto = AIMapper.response_to_dto(response)

    assert dto.created_at == response.created_at


# ==========================================================
# Response Id Mapping
# ==========================================================

def test_response_id_mapping():
    response = create_response()

    dto = AIMapper.response_to_dto(response)

    assert dto.response_id == str(response.id)


# ==========================================================
# Value Object Preservation
# ==========================================================

def test_value_objects_are_preserved():
    dto = AIRequestDTO(
        provider="openai",
        model="gpt-4.1",
        prompt="Test",
        temperature=1.2,
        max_tokens=512,
    )

    request = AIMapper.dto_to_domain(dto)

    assert request.provider.value == "openai"
    assert request.model.value == "gpt-4.1"
    assert request.prompt.value == "Test"
    assert request.temperature.value == 1.2
    assert request.max_tokens.value == 512


# ==========================================================
# Total Token Calculation
# ==========================================================

def test_total_tokens_are_calculated():
    usage = TokenUsage(
        prompt_tokens=10,
        completion_tokens=15,
    )

    assert usage.total_tokens == 25


# ==========================================================
# End-to-End Mapping
# ==========================================================

def test_end_to_end_mapping():
    command = create_command()

    dto = AIMapper.command_to_dto(command)

    request = AIMapper.dto_to_domain(dto)

    assert request.provider.value == command.provider
    assert request.model.value == command.model
    assert request.prompt.value == command.prompt