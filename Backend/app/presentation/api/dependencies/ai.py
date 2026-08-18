from typing import Annotated

from fastapi import Depends


class AIService:
    """
    Minimal AI service marker used for dependency typing.
    """

    pass


def get_ai_dependency() -> AIService:
    """
    Resolve the AI service.
    """
    return AIService()


AIServiceDependency = Annotated[
    AIService,
    Depends(get_ai_dependency),
]
