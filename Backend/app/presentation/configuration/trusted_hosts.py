from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def configure_trusted_hosts(app: FastAPI) -> None:
    """
    Configure trusted hosts.
    """

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],  # Replace in production
    )