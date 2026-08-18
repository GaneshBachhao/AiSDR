"""
Presentation exception handlers.
"""

from fastapi import FastAPI

from .application_handler import (
    register_application_exception_handlers,
)
from .domain_handler import register_domain_exception_handlers
from .validation_handler import register_validation_exception_handlers


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.
    """
    register_application_exception_handlers(app)
    register_validation_exception_handlers(app)
    register_domain_exception_handlers(app)
