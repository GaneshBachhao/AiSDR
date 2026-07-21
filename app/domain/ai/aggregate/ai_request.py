from datetime import UTC, datetime
from typing import List, Optional
from uuid import uuid4

from domain.shared.base import AggregateRoot

from ..entities.ai_message import AIMessage
from ..entities.ai_response import AIResponse
from ..enums.ai_request_status import AIRequestStatus
from ..events.ai_request_completed import AIRequestCompleted
from ..events.ai_request_created import AIRequestCreated
from ..events.ai_request_failed import AIRequestFailed
from ..events.ai_request_started import AIRequestStarted
from ..events.ai_response_received import AIResponseReceived
from ..exceptions.ai_exception import AIException
from ..exceptions.invalid_ai_request_state import InvalidAIRequestState
from ..value_objects.ai_request_id import AIRequestId
from ..value_objects.max_tokens import MaxTokens
from ..value_objects.model_name import ModelName
from ..value_objects.provider_name import ProviderName
from ..value_objects.temperature import Temperature


class AIRequest(AggregateRoot[AIRequestId]):
    """
    Aggregate Root representing a single AI interaction.
    """

    def __init__(
        self,
        provider: ProviderName,
        model: ModelName,
        temperature: Temperature,
        max_tokens: MaxTokens,
        request_id: Optional[AIRequestId] = None,
    ):
        request_id = request_id or AIRequestId(uuid4())

        super().__init__(request_id)

        self._provider = provider
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

        self._status = AIRequestStatus.PENDING

        self._messages: List[AIMessage] = []

        self._response: Optional[AIResponse] = None

        self._completed_at: Optional[datetime] = None

        self.add_domain_event(
            AIRequestCreated(self.id)
        )

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def provider(self) -> ProviderName:
        return self._provider

    @property
    def model(self) -> ModelName:
        return self._model

    @property
    def temperature(self) -> Temperature:
        return self._temperature

    @property
    def max_tokens(self) -> MaxTokens:
        return self._max_tokens

    @property
    def status(self) -> AIRequestStatus:
        return self._status

    @property
    def messages(self) -> List[AIMessage]:
        return list(self._messages)

    @property
    def response(self) -> Optional[AIResponse]:
        return self._response

    @property
    def completed_at(self) -> Optional[datetime]:
        return self._completed_at

    # --------------------------------------------------
    # Message Management
    # --------------------------------------------------

    def add_message(
        self,
        message: AIMessage,
    ) -> None:

        if self._status != AIRequestStatus.PENDING:
            raise InvalidAIRequestState(
                "Messages can only be added before execution."
            )

        self._messages.append(message)
        self.touch()

    # --------------------------------------------------
    # Execution Lifecycle
    # --------------------------------------------------

    def start(self) -> None:

        if self._status != AIRequestStatus.PENDING:
            raise InvalidAIRequestState(
                "Only pending requests can be started."
            )

        if not self._messages:
            raise AIException(
                "AI request must contain at least one message."
            )

        self._status = AIRequestStatus.RUNNING

        self.touch()

        self.add_domain_event(
            AIRequestStarted(self.id)
        )

    def attach_response(
        self,
        response: AIResponse,
    ) -> None:

        if self._status != AIRequestStatus.RUNNING:
            raise InvalidAIRequestState(
                "Response can only be attached while request is running."
            )

        self._response = response

        self.touch()

        self.add_domain_event(
            AIResponseReceived(
                self.id,
                response.id,
            )
        )

    def complete(self) -> None:

        if self._status != AIRequestStatus.RUNNING:
            raise InvalidAIRequestState(
                "Only running requests can be completed."
            )

        if self._response is None:
            raise AIException(
                "Cannot complete request without a response."
            )

        self._status = AIRequestStatus.COMPLETED
        self._completed_at = datetime.now(UTC)

        self.touch()

        self.add_domain_event(
            AIRequestCompleted(self.id)
        )

    def fail(self) -> None:

        if self._status != AIRequestStatus.RUNNING:
            raise InvalidAIRequestState(
                "Only running requests can fail."
            )

        self._status = AIRequestStatus.FAILED
        self._completed_at = datetime.now(UTC)

        self.touch()

        self.add_domain_event(
            AIRequestFailed(
                self.id,
                "AI request execution failed.",
            )
        )

    def cancel(self) -> None:

        if self._status == AIRequestStatus.COMPLETED:
            raise InvalidAIRequestState(
                "Completed requests cannot be cancelled."
            )

        self._status = AIRequestStatus.CANCELLED
        self._completed_at = datetime.now(UTC)

        self.touch()

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    def has_response(self) -> bool:
        return self._response is not None

    def is_completed(self) -> bool:
        return self._status == AIRequestStatus.COMPLETED