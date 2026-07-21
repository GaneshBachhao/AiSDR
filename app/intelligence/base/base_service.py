"""
Base Intelligence Service

Shared functionality for all AI BDOS intelligence services.
"""

import logging


class BaseService:
    """
    Base class for all AI BDOS services.

    Provides common lifecycle management
    and logging functionality.
    """

    # ------------------------------------------------------------------
    # Service Metadata
    # ------------------------------------------------------------------

    name: str = "BaseService"
    version: str = "1.0.0"
    description: str = ""

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            self.__class__.__name__,
        )

    @property
    def service_type(self) -> str:
        """
        Returns the concrete service type.
        """
        return self.__class__.__name__

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """
        Initialize service resources.
        """
        pass

    def shutdown(self) -> None:
        """
        Cleanup service resources.
        """
        pass

    # ------------------------------------------------------------------
    # Logging Helpers
    # ------------------------------------------------------------------

    def log_debug(
        self,
        message: str,
    ) -> None:
        self.logger.debug(message)

    def log_info(
        self,
        message: str,
    ) -> None:
        self.logger.info(message)

    def log_warning(
        self,
        message: str,
    ) -> None:
        self.logger.warning(message)

    def log_error(
        self,
        message: str,
    ) -> None:
        self.logger.error(message)

    def log_exception(
        self,
        message: str,
    ) -> None:
        self.logger.exception(message)