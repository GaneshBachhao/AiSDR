# app/application/common/interfaces/file_storage.py

"""
File storage application port.

Infrastructure handles filesystem, S3, Azure Blob, or other
storage implementations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class FileStorage(ABC):
    """
    Contract for file storage operations.
    """

    @abstractmethod
    async def upload(
        self,
        *,
        filename: str,
        content: bytes,
        content_type: str,
    ) -> str:
        """
        Store a file and return its location.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        *,
        location: str,
    ) -> None:
        """
        Remove stored file.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        *,
        location: str,
    ) -> bool:
        """
        Check file existence.
        """
        raise NotImplementedError