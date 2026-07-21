"""
Configuration Manager

Central configuration access point for AI BDOS.
"""

from typing import Any
from typing import Dict
from typing import Optional

from common.configuration.configuration_result import (
    ConfigurationResult,
)


class ConfigurationManager:
    """
    Central configuration manager.

    Stores and retrieves configuration values
    independent of their source.
    """

    def __init__(self) -> None:
        self._configuration: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Configuration Management
    # ------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a configuration value.
        """
        self._configuration[key] = value

    def get(
        self,
        key: str,
    ) -> ConfigurationResult[Any]:
        """
        Retrieve a configuration value.
        """
        if key not in self._configuration:
            return ConfigurationResult.failure(
                f"Configuration '{key}' was not found."
            )

        return ConfigurationResult.success_result(
            self._configuration[key],
            source="memory",
        )

    def get_or_default(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> ConfigurationResult[Any]:
        """
        Retrieve a configuration value or
        return the supplied default.
        """
        if key in self._configuration:
            return ConfigurationResult.success_result(
                self._configuration[key],
                source="memory",
            )

        return ConfigurationResult.success_result(
            default,
            source="default",
        )

    def contains(
        self,
        key: str,
    ) -> bool:
        """
        Check whether a configuration exists.
        """
        return key in self._configuration

    def remove(
        self,
        key: str,
    ) -> None:
        """
        Remove a configuration value.
        """
        self._configuration.pop(key, None)

    def clear(self) -> None:
        """
        Remove all configuration values.
        """
        self._configuration.clear()