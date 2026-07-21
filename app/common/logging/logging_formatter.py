"""
Logging Formatter

Factory for creating standard AI BDOS log formatters.
"""

import logging

from common.logging.logging_configuration import (
    LoggingConfiguration,
)


class LoggingFormatter:
    """
    Factory for creating configured logging formatters.
    """

    @staticmethod
    def create(
        configuration: LoggingConfiguration,
    ) -> logging.Formatter:
        """
        Create a configured logging formatter.

        Parameters
        ----------
        configuration
            Logging configuration.

        Returns
        -------
        logging.Formatter
            Configured formatter instance.
        """

        return logging.Formatter(
            fmt=configuration.format,
            datefmt=configuration.date_format,
        )