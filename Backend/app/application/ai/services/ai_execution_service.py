"""
Application service responsible for executing AI requests.
"""

from __future__ import annotations

from app.application.ai.ports import AIProvider, AIUsageRecorder
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse


class AIExecutionService:
    """
    Coordinates execution of AI requests.
    """

    def __init__(
        self,
        provider: AIProvider,
        usage_recorder: AIUsageRecorder | None = None,
    ) -> None:
        self._provider = provider
        self._usage_recorder = usage_recorder

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute an AI request.

        Workflow

        CREATED
            ↓
        IN_PROGRESS
            ↓
        Provider
            ↓
        COMPLETED / FAILED

        Usage is logged in ``finally`` -- on both success and failure, since
        a failed call still consumes quota against the provider's budget.
        """

        request.start()

        try:
            response = await self._provider.execute(
                request,
            )

            request.complete(
                response,
            )

            return response

        except Exception as ex:
            request.fail(
                str(ex),
            )

            raise

        finally:
            if self._usage_recorder is not None:
                await self._usage_recorder.log(request)

    async def health_check_all(
        self,
    ) -> dict[str, bool]:
        """
        Check health of every configured provider.
        """

        return await self._provider.health_check_all()
