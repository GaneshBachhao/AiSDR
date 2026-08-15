from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.ai.entities.ai_message import AIMessage
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.enums.ai_request_status import AIRequestStatus
from app.domain.ai.value_objects.ai_request_id import AIRequestId
from app.domain.ai.value_objects.max_tokens import MaxTokens
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.prompt import Prompt
from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.ai.value_objects.temperature import Temperature
from app.domain.shared.base.aggregate_root import AggregateRoot


@dataclass(eq=False)
class AIRequest(AggregateRoot[AIRequestId]):
    """
    Aggregate root representing an AI request lifecycle.
    """

    id: AIRequestId = field(
        default_factory=AIRequestId,
        kw_only=True,
    )

    provider: ProviderName

    model: ModelName

    prompt: Prompt

    temperature: Temperature = field(
        default_factory=Temperature,
    )

    max_tokens: MaxTokens = field(
        default_factory=MaxTokens,
    )

    status: AIRequestStatus = AIRequestStatus.CREATED

    messages: list[AIMessage] = field(
        default_factory=list,
    )

    response: AIResponse | None = None

    failure_reason: str | None = None

    started_at: datetime | None = None

    completed_at: datetime | None = None

    def start(self) -> None:
        """
        Marks the request as executing.
        """

        if self.status != AIRequestStatus.CREATED:
            raise ValueError(
                "Only newly created requests can be started."
            )

        self.status = AIRequestStatus.IN_PROGRESS
        self.started_at = datetime.now(UTC)
        self.touch()

    def complete(
        self,
        response: AIResponse,
    ) -> None:
        """
        Completes the request successfully.
        """

        if self.status != AIRequestStatus.IN_PROGRESS:
            raise ValueError(
                "Only executing requests can be completed."
            )

        self.response = response
        self.status = AIRequestStatus.COMPLETED
        self.completed_at = datetime.now(UTC)
        self.touch()

    def fail(
        self,
        reason: str,
    ) -> None:
        """
        Marks the request as failed.
        """

        if self.status != AIRequestStatus.IN_PROGRESS:
            raise ValueError(
                "Only executing requests can fail."
            )

        self.failure_reason = reason.strip()
        self.status = AIRequestStatus.FAILED
        self.completed_at = datetime.now(UTC)
        self.touch()

    def add_message(
        self,
        message: AIMessage,
    ) -> None:
        """
        Adds a conversation message.
        """

        self.messages.append(message)
        self.touch()

    @property
    def is_completed(self) -> bool:
        return (
            self.status
            == AIRequestStatus.COMPLETED
        )

    @property
    def is_failed(self) -> bool:
        return (
            self.status
            == AIRequestStatus.FAILED
        )

    @property
    def can_execute(self) -> bool:
        return (
            self.status
            == AIRequestStatus.CREATED
        )