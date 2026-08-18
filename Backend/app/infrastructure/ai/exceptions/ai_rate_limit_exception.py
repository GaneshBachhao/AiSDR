from __future__ import annotations

from .ai_client_exception import AIClientException


class AIRateLimitException(AIClientException):
    """The AI provider itself reported a rate-limit/quota error (e.g.
    Gemini's ``429 RESOURCE_EXHAUSTED``) -- distinct from a malformed
    request, an auth failure, or a provider outage, since a rate limit is
    expected to recover once the window/quota resets rather than
    indicating something is actually broken.

    Subclasses ``AIClientException`` (not a new, unrelated exception type)
    so every existing ``except AIClientException``/``except
    _RECOVERABLE_ERRORS`` site upstream keeps working unchanged; callers
    that specifically want to distinguish a rate limit can catch this
    subclass instead.
    """

    def __init__(self, message: str, retry_after_seconds: float | None = None) -> None:
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds
