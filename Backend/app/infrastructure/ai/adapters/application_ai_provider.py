"""
Infrastructure adapter implementing the
Application AIProvider port.
"""

from __future__ import annotations

from app.application.ai.ports import AIProvider
from app.domain.ai.aggregates.ai_request import AIRequest
from app.domain.ai.entities.ai_response import AIResponse
from app.domain.ai.value_objects.model_name import ModelName
from app.domain.ai.value_objects.provider_name import ProviderName
from app.infrastructure.ai.exceptions.ai_client_exception import (
    AIClientException,
)
from app.infrastructure.ai.exceptions.ai_provider_exception import (
    AIProviderException,
)
from app.infrastructure.ai.providers.base_provider import (
    BaseAIProvider,
)
from app.infrastructure.ai.usage.ai_rate_limiter import AIRateLimiter

_RECOVERABLE_ERRORS = (
    AIProviderException,
    AIClientException,
)


class ApplicationAIProvider(AIProvider):
    """
    Routes AI requests to the configured provider.

    Optionally falls back to an ordered list of alternate providers when
    the primary provider raises a recoverable error (e.g. a deprecated
    model, an exhausted quota) -- so one provider's outage doesn't fail
    an entire batch. Fallback is a no-op unless both ``fallback_order``
    and ``default_models`` are supplied.

    Optionally throttles calls per concrete provider via ``rate_limiter``
    (a requests-per-minute gate, distinct from AIBudgetGuard's daily
    total) -- each of the up to two outbound calls per ``execute()``
    (primary, then one fallback) is gated by the provider actually being
    called, so a fallback to a different provider is never throttled
    against the primary's bucket.
    """

    def __init__(
        self,
        providers: dict[str, BaseAIProvider],
        fallback_order: list[str] | None = None,
        default_models: dict[str, str] | None = None,
        rate_limiter: AIRateLimiter | None = None,
    ) -> None:

        self._providers = providers
        self._fallback_order = [name.lower() for name in (fallback_order or [])]
        self._default_models = default_models or {}
        self._rate_limiter = rate_limiter

    async def execute(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Execute request using the selected provider, falling back to the
        next configured provider in ``fallback_order`` on a recoverable
        error.
        """

        provider_name = request.provider.value.lower()

        provider = self._providers.get(
            provider_name,
        )

        if provider is None:
            raise ValueError(f"Unsupported AI provider: {provider_name}")

        attempted = {provider_name}

        try:
            if self._rate_limiter is not None:
                await self._rate_limiter.acquire(provider_name)
            return await provider.execute(request)
        except _RECOVERABLE_ERRORS as primary_error:
            last_error = primary_error

        for fallback_name in self._fallback_order:
            if fallback_name in attempted:
                continue

            attempted.add(fallback_name)

            fallback_provider = self._providers.get(fallback_name)
            fallback_model = self._default_models.get(fallback_name)

            if fallback_provider is None or not fallback_model:
                continue

            fallback_request = AIRequest(
                provider=ProviderName(fallback_name),
                model=ModelName(fallback_model),
                prompt=request.prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            try:
                if self._rate_limiter is not None:
                    await self._rate_limiter.acquire(fallback_name)
                return await fallback_provider.execute(fallback_request)
            except _RECOVERABLE_ERRORS as fallback_error:
                last_error = fallback_error
                continue

        raise last_error

    async def health_check(
        self,
        provider_name: str,
    ) -> bool:
        """
        Check health of a specific provider.
        """

        provider = self._providers.get(
            provider_name.lower(),
        )

        if provider is None:
            return False

        return await provider.health_check()

    async def health_check_all(
        self,
    ) -> dict[str, bool]:
        """
        Check health of every configured provider.
        """

        return {name: await self.health_check(name) for name in self._providers}
