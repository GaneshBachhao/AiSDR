"""
Base HTTP client contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from .http_response import HttpResponse


class BaseHttpClient(ABC):
    """
    Contract for HTTP communication.
    """

    @abstractmethod
    async def get(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    async def post(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    async def put(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    async def patch(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        raise NotImplementedError

    @abstractmethod
    async def health_check(
        self,
        url: str,
    ) -> bool:
        raise NotImplementedError