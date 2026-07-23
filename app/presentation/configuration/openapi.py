from fastapi import FastAPI


def configure_openapi(app: FastAPI) -> None:
    """
    Configure OpenAPI metadata.
    """

    app.title = "PamaCore Labs API"
    app.description = "AI Consulting Platform"
    app.version = "1.0.0"
    app.contact = {
        "name": "PamaCore Labs",
    }