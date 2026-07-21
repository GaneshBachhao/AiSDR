"""
Metadata Manager

Central application metadata manager.
"""

from common.metadata.application_metadata import (
    ApplicationMetadata,
)


class MetadataManager:
    """
    Central metadata manager.

    Provides access to application metadata.
    """

    _metadata = ApplicationMetadata()

    @classmethod
    def configure(
        cls,
        metadata: ApplicationMetadata,
    ) -> None:
        """
        Configure application metadata.
        """
        cls._metadata = metadata

    @classmethod
    def get(
        cls,
    ) -> ApplicationMetadata:
        """
        Retrieve the current application metadata.
        """
        return cls._metadata

    @classmethod
    def reset(
        cls,
    ) -> None:
        """
        Reset metadata to default values.

        Primarily intended for testing.
        """
        cls._metadata = ApplicationMetadata()