from app.exceptions.custom_exceptions import (
    AgneticAIException,
    LeadNotFoundException,
    DuplicateLeadException,
)

from app.exceptions.handlers import register_exception_handlers