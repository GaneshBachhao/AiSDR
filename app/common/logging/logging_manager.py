"""
Logging Manager

Central logging manager for AI BDOS.
"""

import logging
from typing import Dict

from common.logging.logging_configuration import (
    LoggingConfiguration,
)
from common.logging.logging_formatter import (
    LoggingFormatter,
)


class LoggingManager:
    """
    Central logging manager.

    Responsible for creating and configuring
    application loggers.
    """

    _configured: bool = False

    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def configure(
        cls,
        configuration: LoggingConfiguration,
    ) -> None:
        """
        Configure the root logging system.

        Safe to call multiple times.
        """

        if cls._configured:
            return

        formatter = LoggingFormatter.create(
            configuration,
        )

        root_logger = logging.getLogger()

        root_logger.setLevel(configuration.level)

        if configuration.enable_console:

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(
                formatter,
            )

            root_logger.addHandler(
                console_handler,
            )

        if configuration.enable_file:

            file_handler = logging.FileHandler(
                configuration.file_name,
            )

            file_handler.setFormatter(
                formatter,
            )

            root_logger.addHandler(
                file_handler,
            )

        cls._configured = True

    @classmethod
    def get_logger(
        cls,
        name: str,
    ) -> logging.Logger:
        """
        Get or create a logger.
        """

        if name not in cls._loggers:

            cls._loggers[name] = logging.getLogger(
                name,
            )

        return cls._loggers[name]

    @classmethod
    def clear(cls) -> None:
        """
        Clear cached loggers.

        Intended for testing.
        """

        cls._loggers.clear()

        cls._configured = False