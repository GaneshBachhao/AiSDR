class TavilyRateLimitException(Exception):
    """Tavily itself reported a rate-limit/usage-cap error
    (``tavily.UsageLimitExceededError``) -- distinct from a malformed
    request, an auth failure, or any other search error, since this one is
    expected to recover once the window/plan limit resets rather than
    indicating something is actually broken.
    """
