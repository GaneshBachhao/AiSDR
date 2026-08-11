from fastapi import APIRouter, status

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
) -> AIResponseSchema:
    """
    Process an AI request.
    """

    return AIResponseSchema(
        content=f"Echo: {request.prompt}",
        provider=request.provider,
        model="mock-model",
        prompt_tokens=len(request.prompt.split()),
        completion_tokens=8,
        total_tokens=len(request.prompt.split()) + 8,
        finish_reason="stop",
    )