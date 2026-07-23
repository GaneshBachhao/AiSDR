from fastapi import APIRouter, status

from app.application.ai.commands.process_ai_request.process_ai_request_command import (
    ProcessAIRequestCommand,
)
from app.application.ai.handlers.process_ai_request_handler import (
    ProcessAIRequestHandler,
)
from app.presentation.api.dependencies.ai import AIServiceDependency
from app.presentation.schemas.requests.ai_request import AIRequestSchema
from app.presentation.schemas.responses.ai_response import AIResponseSchema

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/chat",
    response_model=AIResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def chat(
    request: AIRequestSchema,
    ai_service: AIServiceDependency,
) -> AIResponseSchema:
    """
    Process an AI request.
    """

    command = ProcessAIRequestCommand(
        prompt=request.prompt,
        provider=request.provider,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    handler = ProcessAIRequestHandler(ai_service)

    result = await handler.handle(command)

    return AIResponseSchema(
        content=result.content,
        provider=result.provider,
        model=result.model,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        total_tokens=result.total_tokens,
        finish_reason=result.finish_reason,
    )