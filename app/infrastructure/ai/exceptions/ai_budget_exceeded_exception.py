class AIBudgetExceededException(Exception):
    """
    Raised when a batch of AI calls would exceed the configured daily
    request budget for a provider. Distinct from ``AIProviderException``:
    this fires before any call is attempted, not because one failed.
    """

    pass
