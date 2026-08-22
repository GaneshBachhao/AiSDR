"""Tests for the SEARCH_PROVIDER flag dispatch (Tavily <-> ddgs)."""

from __future__ import annotations

from app.infrastructure.configuration.search_provider_settings import (
    SearchProviderSettings,
)
from app.integrations.ddgs.ddgs_client import DdgsClient
from app.integrations.tavily.tavily_client import AgneticTavilyClient
from app.presentation.api.dependencies.company_research import resolve_search_client


def test_defaults_to_tavily_when_unconfigured() -> None:
    client = resolve_search_client(SearchProviderSettings(search_provider=""))
    assert isinstance(client, AgneticTavilyClient)


def test_resolves_to_tavily_explicitly() -> None:
    client = resolve_search_client(SearchProviderSettings(search_provider="tavily"))
    assert isinstance(client, AgneticTavilyClient)


def test_resolves_to_ddgs_when_flag_is_set() -> None:
    client = resolve_search_client(SearchProviderSettings(search_provider="ddgs"))
    assert isinstance(client, DdgsClient)


def test_flag_is_case_and_whitespace_insensitive() -> None:
    client = resolve_search_client(SearchProviderSettings(search_provider="  DDGS  "))
    assert isinstance(client, DdgsClient)
