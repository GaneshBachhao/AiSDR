"""
Application Custom Exceptions

Centralized exception hierarchy for the AI SDR platform.
"""


# ==========================================================
# Base Exception
# ==========================================================

class AgneticAIException(Exception):
    """
    Base exception for the entire application.
    """

    def __init__(
        self,
        message: str,
    ):
        self.message = message
        super().__init__(message)


# ==========================================================
# Lead Exceptions
# ==========================================================

class LeadException(AgneticAIException):
    """
    Base exception for Lead operations.
    """
    pass


class LeadNotFoundException(
    LeadException,
):
    """
    Raised when a Lead cannot be found.
    """

    def __init__(
        self,
        lead_id: int,
    ):
        super().__init__(
            f"Lead with ID {lead_id} was not found."
        )


class DuplicateLeadException(
    LeadException,
):
    """
    Raised when attempting to create
    a duplicate Lead.
    """

    def __init__(
        self,
        value: str,
    ):
        super().__init__(
            f"Lead already exists: {value}"
        )


# ==========================================================
# Discovery Exceptions
# ==========================================================

class DiscoveryException(
    AgneticAIException,
):
    """
    Base exception for Discovery.
    """
    pass


class UnsupportedDiscoveryProviderException(
    DiscoveryException,
):
    """
    Raised when an unsupported
    Discovery Provider is configured.
    """

    def __init__(
        self,
        provider: str,
    ):
        super().__init__(
            f"Unsupported Discovery Provider: {provider}"
        )


# ==========================================================
# LLM Exceptions
# ==========================================================

class LLMException(
    AgneticAIException,
):
    """
    Base exception for all
    LLM integrations.
    """
    pass


class GeminiConfigurationException(
    LLMException,
):
    """
    Gemini configuration is invalid.
    """
    pass


class GeminiAPIException(
    LLMException,
):
    """
    Gemini API returned an error.
    """
    pass


class GeminiGenerationException(
    LLMException,
):
    """
    Gemini failed to generate content.
    """
    pass


class GeminiAuthenticationException(
    LLMException,
):
    """
    Gemini authentication failed.
    """
    pass


class GeminiRateLimitException(
    LLMException,
):
    """
    Gemini rate limit exceeded.
    """
    pass


class GeminiResponseParseException(
    LLMException,
):
    """
    Gemini response could not be parsed.
    """
    pass