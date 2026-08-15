"""
Tavily-backed implementation of ``ContactDiscoveryPort``.

Only runs for candidates that have already passed identity verification and
cleared ``minimum_qualification_score`` (enforced by the caller). Searches
for the target company's public LinkedIn profiles and mines the search
result titles for a name + title -- never fabricates a contact if no
qualifying profile page is found.
"""

from __future__ import annotations

import asyncio
from urllib.parse import urlparse

from app.application.company_research.dto.company_research_response import (
    DiscoveredContact,
)
from app.application.company_research.ports.contact_discovery_port import (
    ContactDiscoveryPort,
)
from app.domain.company_research.entities.candidate import CompanyCandidate
from app.infrastructure.configuration.company_research_settings import (
    CompanyResearchSettings,
)
from app.integrations.tavily.tavily_client import AgneticTavilyClient

_DEFAULT_TARGET_ROLE_TERMS = "CTO OR CIO OR COO OR founder OR VP"


class TavilyContactDiscoveryAdapter(ContactDiscoveryPort):
    """Discovers decision-maker contacts for a qualified company via Tavily."""

    def __init__(
        self,
        client: AgneticTavilyClient | None = None,
        settings: CompanyResearchSettings | None = None,
    ) -> None:
        self._client = client or AgneticTavilyClient()
        self._settings = settings or CompanyResearchSettings()

    async def discover(
        self,
        candidate: CompanyCandidate,
        website: str | None,
        target_role: str | None,
    ) -> list[DiscoveredContact]:
        return await asyncio.to_thread(self._discover, candidate, target_role)

    def _discover(
        self,
        candidate: CompanyCandidate,
        target_role: str | None,
    ) -> list[DiscoveredContact]:
        name = candidate.company_name
        role_terms = target_role or _DEFAULT_TARGET_ROLE_TERMS
        max_contacts = self._settings.max_contacts_per_candidate

        queries = [
            f'"{name}" {role_terms} LinkedIn profile',
            f'"{name}" leadership team {role_terms}',
        ]

        contacts: list[DiscoveredContact] = []
        seen_names: set[str] = set()

        for query in queries:
            for item in self._client.search(query=query, max_results=5, search_depth="basic"):
                url = str(item.get("url", "")).strip()
                title = str(item.get("title", "")).strip()
                if not url or not title or not self._is_linkedin_profile(url):
                    continue

                parsed = self._parse_person_and_title(title)
                if parsed is None:
                    continue
                person_name, role_title = parsed

                normalized = person_name.lower()
                if normalized in seen_names:
                    continue
                seen_names.add(normalized)

                contacts.append(
                    DiscoveredContact(
                        name=person_name,
                        role_title=role_title,
                        linkedin_url=url,
                        source_url=url,
                    )
                )
                if len(contacts) >= max_contacts:
                    return contacts

        return contacts

    @staticmethod
    def _is_linkedin_profile(url: str) -> bool:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().removeprefix("www.")
        return domain == "linkedin.com" and parsed.path.startswith("/in/")

    @staticmethod
    def _parse_person_and_title(title: str) -> tuple[str, str | None] | None:
        """Parse a LinkedIn search-result title like
        ``"John Smith - Chief Technology Officer - Acme Corp | LinkedIn"``
        into ``("John Smith", "Chief Technology Officer")``.
        """
        cleaned = title
        for marker in (" | LinkedIn", "| LinkedIn", " - LinkedIn"):
            if marker in cleaned:
                cleaned = cleaned.split(marker, 1)[0].strip()
                break

        parts = [part.strip() for part in cleaned.split(" - ") if part.strip()]
        if not parts:
            return None

        person_name = parts[0]
        if not person_name or len(person_name.split()) > 5 or len(person_name) < 3:
            return None

        role_title = parts[1] if len(parts) > 1 else None
        return person_name, role_title
