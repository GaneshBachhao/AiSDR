from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


def configure_gzip(app: FastAPI) -> None:
    """
    Configure GZip compression.
    """

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1024,
    )
