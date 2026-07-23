from typing import Annotated

from fastapi import Depends

from app.application.ai.interfaces.ai_service import AIService
from app.infrastructure.di.provider import get_ai_service


def get_ai_dependency() -> AIService:
    """
    Resolve the AI service.
    """
    return get_ai_service()


AIServiceDependency = Annotated[
    AIService,
    Depends(get_ai_dependency),
]