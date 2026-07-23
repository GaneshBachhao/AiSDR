from fastapi import FastAPI


API_VERSION = "v1"


def configure_versioning(app: FastAPI) -> None:
    """
    Configure API versioning metadata.
    """

    app.version = API_VERSION