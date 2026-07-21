from enum import Enum


class JobType(str, Enum):
    """
    Supported job types within AgneticAI.
    """

    DISCOVERY = "DISCOVERY"

    RESEARCH = "RESEARCH"

    PROPOSAL = "PROPOSAL"

    EMAIL = "EMAIL"

    FOLLOW_UP = "FOLLOW_UP"

    IMPORT = "IMPORT"

    EXPORT = "EXPORT"

    SYSTEM = "SYSTEM"