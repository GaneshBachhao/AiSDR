"""
Source Types

Identifies where business intelligence originates.
"""

from enum import Enum


class SourceType(str, Enum):

    EMAIL = "EMAIL"

    WEBSITE = "WEBSITE"

    LINKEDIN = "LINKEDIN"

    CRM = "CRM"

    DOCUMENT = "DOCUMENT"

    CHAT = "CHAT"

    API = "API"

    MANUAL = "MANUAL"