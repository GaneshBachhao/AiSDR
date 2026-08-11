from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import re
from urllib.parse import urlparse

from app.company_research.providers.base_provider import CompanyResearchProvider
from app.company_research.schemas.company_research import (
    CompanyResearchRequest,
    CompanySearchResult,
    EvidenceItem,
)
from app.integrations.tavily.tavily_client import AgneticTavilyClient
from app.company_research.funnel.candidate import DiscoveryCandidate
from app.company_research.funnel.pipeline import DiscoveryFunnel


class TavilyCompanyResearchProvider(CompanyResearchProvider):
    """Public-web provider with identity, industry and controlled parallel research."""

    _GENERIC_TITLE_MARKERS = (
        "top ", "best ", "list of", "companies in", "companies using",
        "companies that", "directory", "market report", "industry report",
        "press release", "news", "blog", "case study", "guide", "how to",
        "jobs", "job openings", "hiring", "events",
    )

    _DISCOVERY_TITLE_MARKERS = (
        "companies in", "companies —", "companies -", "records", "business directory",
        "company directory", "company database", "manufacturing database",
    )

    _INDUSTRY_KEYWORDS = {
        "manufacturing": (
            "manufacturer", "manufacturing", "factory", "production plant",
            "industrial machinery", "industrial equipment", "automotive manufacturer",
            "electronics manufacturing", "component manufacturer", "fabrication",
            "machinery maker", "production facility",
        ),
        "information technology": (
            "software company", "software development", "it services", "information technology",
            "technology services", "saas", "software as a service", "cloud services",
            "systems integrator", "managed services", "technology consulting",
        ),
        "software": (
            "software company", "software development", "saas", "software platform",
            "enterprise software", "software products",
        ),
        "healthcare": (
            "healthcare provider", "healthcare company", "hospital", "clinic", "health system",
            "patient care", "medical center",
        ),
        "hospitals": ("hospital", "medical center", "health system"),
        "pharma": ("pharmaceutical", "pharma", "biotechnology", "biotech", "drug manufacturer"),
        "biotechnology": ("biotechnology", "biotech", "life sciences"),
        "financial services": ("bank", "banking", "financial services", "fintech", "lending"),
        "insurance": ("insurance company", "insurer", "insurance provider"),
        "logistics": ("logistics", "freight", "transportation", "warehousing", "supply chain"),
        "retail": ("retailer", "retail company", "e-commerce", "ecommerce", "online retailer"),
        "real estate": ("real estate", "property developer", "property management", "realty"),
        "construction": ("construction company", "contractor", "engineering and construction"),
        "travel": ("travel company", "tour operator", "travel agency", "hospitality"),
        "hospitality": ("hotel", "hospitality", "resort", "restaurant group"),
        "energy": ("energy company", "utility", "power generation", "renewable energy", "oil and gas"),
        "agriculture": ("agriculture", "agricultural", "agribusiness", "farm", "crop producer"),
        "telecommunications": ("telecommunications", "telecom", "mobile network", "internet service provider"),
        "education": ("university", "college", "education provider", "school", "edtech"),
        "research": ("research institute", "research organization", "laboratory", "r&d center"),
    }

    _NEGATIVE_SERVICE_MARKERS = (
        "it services", "software company", "software development", "technology consulting",
        "ai company", "automation vendor", "cloud consulting", "digital agency",
        "system integrator", "managed services", "staffing", "recruitment agency",
    )

    def __init__(self) -> None:
        self.client = AgneticTavilyClient()
        self._funnel = DiscoveryFunnel()

    def discover(self, request: CompanyResearchRequest) -> list[CompanySearchResult]:
        candidates = self._discover_candidates(request)
        if not candidates:
            return []

        max_workers = min(6, max(1, len(candidates)))
        results: list[CompanySearchResult] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._research_candidate, candidate, request): candidate
                for candidate in candidates
            }
            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception:
                    continue
                if result is None:
                    continue
                if result.qualification_score < request.minimum_qualification_score:
                    continue
                results.append(result)
                if len(results) >= request.number_of_companies:
                    # Remaining futures are allowed to finish cleanly; no more results are needed.
                    break

        results.sort(key=lambda item: item.qualification_score, reverse=True)
        return results[: request.number_of_companies]

    def _discover_candidates(self, request: CompanyResearchRequest) -> list[dict]:
        """Discover real companies while also using directory/search pages as candidate sources.

        A directory page is never returned as a company. Its current title, record count,
        URL and extracted company names are retained as dynamic discovery metadata so a
        future run can use whatever count/title the source currently exposes.
        """
        industries = request.industries or ["companies"]
        queries: list[str] = []

        for industry in industries:
            base = f"{industry} companies in {request.geography} official company website"
            if request.company_size:
                base += " " + " ".join(request.company_size[:3])
            queries.extend(
                [
                    base,
                    f"{industry} manufacturers companies {request.geography} official website"
                    if industry.lower() == "manufacturing"
                    else f"{industry} companies {request.geography} products services official website",
                    f"{industry} companies {request.geography} expansion hiring technology",
                    f"{industry} companies {request.geography} directory database records",
                ]
            )

        candidates: list[dict] = []
        seen_domains: set[str] = set()
        seen_names: set[str] = set()
        discovery_sources: dict[str, dict] = {}
        target_pool = min(max(request.number_of_companies * 5, 20), 80)

        for query in queries:
            for item in self.client.search(
                query=query,
                max_results=min(target_pool, 30),
                search_depth="basic",
            ):
                url = str(item.get("url", "")).strip()
                title = str(item.get("title", "")).strip()
                content = str(item.get("content", "")).strip()
                if not url or not title:
                    continue

                domain = urlparse(url).netloc.lower().removeprefix("www.")
                if not domain or self._blocked_domain(domain):
                    continue

                discovery = self._discovery_metadata(title, url, content)
                if discovery:
                    key = url
                    discovery_sources[key] = discovery
                    for extracted in self._extract_directory_candidates(content, request.geography):
                        self._append_candidate(
                            candidates, seen_names, seen_domains, extracted,
                            source_metadata=discovery,
                        )
                    continue

                if self._looks_like_article_title(title) or domain in seen_domains:
                    continue

                name = self._candidate_name(title, domain)
                if self._invalid_candidate_name(name):
                    continue
                normalized_name = self._normalize_name(name)
                if normalized_name in seen_names:
                    continue

                seen_names.add(normalized_name)
                seen_domains.add(domain)
                candidates.append(
                    {
                        "company_name": name,
                        "website": self._root_url(url),
                        "title": title,
                        "content": content,
                        "url": url,
                        "discovery_metadata": [],
                    }
                )

                if len(candidates) >= target_pool:
                    return self._apply_deterministic_gate(candidates)

        return self._apply_deterministic_gate(candidates)

    def _apply_deterministic_gate(self, candidates: list[dict]) -> list[dict]:
        """Apply the hard pre-verification gate before any candidate research call."""
        normalized: list[DiscoveryCandidate] = []
        for candidate in candidates:
            metadata = candidate.get("discovery_metadata") or []
            source_url = candidate.get("url") or (metadata[0].get("source_url") if metadata else "")
            normalized.append(
                DiscoveryCandidate(
                    company_name=str(candidate.get("company_name", "")).strip(),
                    website=candidate.get("website"),
                    title=str(candidate.get("title", "")).strip(),
                    content=str(candidate.get("content", "")),
                    source_url=str(source_url or ""),
                    discovery_metadata=metadata,
                )
            )
        accepted, _metrics = self._funnel.gate_candidates(normalized)
        accepted_keys = {id(item) for item in accepted}
        return [
            candidate
            for candidate, normalized_candidate in zip(candidates, normalized)
            if id(normalized_candidate) in accepted_keys
        ]

    @classmethod
    def _append_candidate(
        cls,
        candidates: list[dict],
        seen_names: set[str],
        seen_domains: set[str],
        candidate: dict,
        source_metadata: dict,
    ) -> None:
        name = str(candidate.get("company_name", "")).strip()
        if not name or cls._invalid_candidate_name(name):
            return
        normalized_name = cls._normalize_name(name)
        if normalized_name in seen_names:
            for existing in candidates:
                if cls._normalize_name(existing.get("company_name", "")) == normalized_name:
                    metadata = existing.setdefault("discovery_metadata", [])
                    if source_metadata not in metadata:
                        metadata.append(source_metadata)
                    return
            return

        domain = urlparse(str(candidate.get("website", ""))).netloc.lower().removeprefix("www.")
        if domain and domain in seen_domains:
            return

        seen_names.add(normalized_name)
        if domain:
            seen_domains.add(domain)
        candidate["discovery_metadata"] = [source_metadata]
        candidates.append(candidate)

    @classmethod
    def _discovery_metadata(cls, title: str, url: str, content: str) -> dict | None:
        normalized = " ".join(title.lower().split())
        count = cls._extract_record_count(f"{title} {content}")
        is_discovery_title = any(marker in normalized for marker in cls._DISCOVERY_TITLE_MARKERS)
        has_many_company_rows = bool(cls._extract_directory_candidates(content, None))
        if not is_discovery_title and not count and not has_many_company_rows:
            return None
        return {
            "source_type": "discovery_directory",
            "source_title": title,
            "source_url": url,
            "discovered_record_count": count,
            "metadata_observed_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _extract_record_count(text: str) -> int | None:
        patterns = (
            r"\b([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)\s+records?\b",
            r"\b([0-9]+(?:\.[0-9]+)?)\s*(million|m)\+?\s+(?:companies|records)\b",
        )
        for index, pattern in enumerate(patterns):
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if not match:
                continue
            if index == 0:
                return int(match.group(1).replace(",", ""))
            return int(float(match.group(1)) * 1_000_000)
        return None

    @classmethod
    def _extract_directory_candidates(cls, content: str, geography: str | None) -> list[dict]:
        if not content:
            return []
        lines = [line.strip(" -*|:") for line in content.splitlines() if line.strip()]
        candidates: list[dict] = []
        for index, line in enumerate(lines):
            if line.lower() != "country":
                continue
            if index == 0:
                continue
            name = lines[index - 1].strip()
            if not cls._looks_like_company_name(name):
                continue
            location_parts: list[str] = []
            for following in lines[index + 1:index + 5]:
                if following.lower() in {"sales revenue ($m)", "sales revenue", "revenue"}:
                    break
                if following.lower() == "country":
                    break
                location_parts.append(following)
                if following.lower() in {"india", "usa", "us", "united states", "uk", "canada"}:
                    break
            location = ", ".join(location_parts).strip(" ,")
            if geography and geography.lower() not in location.lower():
                # Some directory formats put country on the next line; if it is not
                # present, retain the candidate only when no geography was requested.
                continue
            candidates.append(
                {
                    "company_name": name,
                    "website": None,
                    "title": name,
                    "content": f"{name}\nCountry: {location}",
                    "url": "",
                }
            )
        return candidates

    @staticmethod
    def _looks_like_company_name(value: str) -> bool:
        value = " ".join(value.split())
        if len(value) < 3 or len(value) > 120:
            return False
        lowered = value.lower()
        if lowered in {"country", "sales revenue ($m)", "sales revenue", "company", "companies"}:
            return False
        if any(marker in lowered for marker in (
            "find manufacturing", "manufacturing companies", "company database",
            "company directory", "records", "search results", "page ",
        )):
            return False
        return sum(char.isalpha() for char in value) >= 3

    @classmethod
    def _invalid_candidate_name(cls, name: str) -> bool:
        normalized = " ".join(name.lower().split())
        return (
            not cls._looks_like_company_name(name)
            or cls._looks_like_article_title(name)
            or normalized.startswith(("find ", "top ", "best ", "list of "))
        )

    @staticmethod
    def _normalize_name(name: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()

    def _research_candidate(self, candidate: dict, request: CompanyResearchRequest) -> CompanySearchResult | None:
        """Verify identity/industry first; only then run deeper research."""
        name = candidate["company_name"]
        target_industries = request.industries

        verification_query = (
            f'"{name}" "{candidate["website"]}" company industry products headquarters employees headcount company size parent'
        )
        verification_items = self.client.search(
            query=verification_query,
            max_results=5,
            search_depth="basic",
        )
        verification_text = " ".join(
            str(item.get("content", "")).strip()
            for item in verification_items
            if item.get("content")
        ).lower()
        verification_title = " ".join(
            str(item.get("title", "")).strip()
            for item in verification_items
        )
        combined_verification = f"{verification_title} {verification_text}"

        industry = self._infer_industry(combined_verification, candidate["title"], target_industries)
        official_website = self._verified_official_website(name, candidate["website"], verification_items)

        industry_match, industry_reason = self._industry_match(
            industry, combined_verification, target_industries
        )
        if target_industries and not industry_match:
            return None

        # ICP size is a hard gate. We intentionally require evidence of employee
        # count when the caller specifies a company-size constraint. Unknown size
        # must not silently pass an SMB/mid-market request.
        size_match, employee_count, size_reason = self._company_size_match(
            combined_verification, request.company_size
        )
        if request.company_size and not size_match:
            return None

        # Reject obvious enterprise-scale organizations/parents before expensive
        # deep research. This is deliberately conservative: a generic word such as
        # "enterprise" is not enough; explicit scale markers are required.
        enterprise_match, parent_company = self._enterprise_exclusion(
            combined_verification, employee_count
        )
        if request.company_size and enterprise_match:
            return None

        evidence: list[EvidenceItem] = []
        seen_urls: set[str] = set()
        for item in verification_items:
            url = str(item.get("url", "")).strip()
            title = str(item.get("title", "")).strip()
            snippet = str(item.get("content", "")).strip()
            if not url or not title or url in seen_urls:
                continue
            seen_urls.add(url)
            evidence.append(
                EvidenceItem(
                    title=title,
                    url=url,
                    snippet=snippet[:800] if snippet else None,
                    evidence_date=(
                        str(item.get("published_date") or item.get("date") or "").strip() or None
                    ),
                )
            )

        period = request.research_period.strip() if request.research_period else "recent"
        queries = [
            f'"{name}" technology AI automation cloud hiring expansion {period}',
            f'"{name}" funding acquisition new product transformation modernization {period}',
        ]
        if request.services:
            queries.append(f'"{name}" ' + " ".join(request.services[:4]) + f" {period}")

        for query in queries:
            for item in self.client.search(query=query, max_results=5, search_depth="advanced"):
                url = str(item.get("url", "")).strip()
                title = str(item.get("title", "")).strip()
                snippet = str(item.get("content", "")).strip()
                if not url or not title or url in seen_urls:
                    continue
                if self._blocked_domain(urlparse(url).netloc.lower()):
                    continue
                seen_urls.add(url)
                evidence.append(
                    EvidenceItem(
                        title=title,
                        url=url,
                        snippet=snippet[:800] if snippet else None,
                        evidence_date=(
                            str(item.get("published_date") or item.get("date") or "").strip() or None
                        ),
                    )
                )
                if len(evidence) >= 8:
                    break
            if len(evidence) >= 8:
                break

        combined = " ".join((item.snippet or "") for item in evidence).lower()
        return self._build_result(
            candidate={
                **candidate,
                "website": official_website,
                "employee_count": employee_count,
                "parent_company": parent_company,
                "icp_match_reason": size_reason,
            },
            evidence=evidence,
            combined=combined,
            request=request,
            actual_industry=industry,
            industry_reason=industry_reason,
        )

    @classmethod
    def _company_size_match(
        cls,
        text: str,
        requested_sizes: list[str],
    ) -> tuple[bool, int | None, str]:
        """Return whether an explicit employee count satisfies the requested ICP size."""
        employee_count = cls._extract_employee_count(text)
        if not requested_sizes:
            return True, employee_count, "No company-size restriction was requested."
        if employee_count is None:
            return False, None, "Employee count could not be verified; size-restricted discovery requires explicit size evidence."

        ranges = [cls._size_range(value) for value in requested_sizes]
        ranges = [item for item in ranges if item is not None]
        if not ranges:
            return False, employee_count, "Requested company-size values are not recognized."
        if any(lower <= employee_count <= upper for lower, upper in ranges):
            return True, employee_count, f"Verified employee count {employee_count} matches the requested company-size range."
        return False, employee_count, f"Verified employee count {employee_count} is outside the requested company-size range."

    @staticmethod
    def _size_range(value: str) -> tuple[int, int] | None:
        normalized = value.strip().lower().replace("–", "-").replace("—", "-")
        match = re.search(r"(\d+)\s*-\s*(\d+)", normalized)
        if match:
            return int(match.group(1)), int(match.group(2))
        if normalized in {"startup", "micro"}:
            return 1, 20
        if normalized in {"small", "small business"}:
            return 21, 50
        if normalized in {"medium", "mid-market", "mid market"}:
            return 51, 500
        if normalized in {"smb", "small and medium business", "small and medium businesses"}:
            return 21, 500
        if normalized == "enterprise":
            return 501, 10_000_000
        return None

    @staticmethod
    def _extract_employee_count(text: str) -> int | None:
        patterns = (
            r"(?:approximately|about|around|over|more than|nearly|total of)?\s*([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{2,7})\s+(?:employees|employee|staff|people|workers)\b",
            r"(?:employees|employee|staff|headcount)\D{0,40}([0-9]{2,7})\b",
            r"headcount\D{0,20}([0-9]{2,7})\b",
        )
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1).replace(",", ""))
                except ValueError:
                    continue
        return None

    @staticmethod
    def _enterprise_exclusion(text: str, employee_count: int | None) -> tuple[bool, str | None]:
        if employee_count is not None and employee_count > 500:
            return True, None
        explicit_markers = (
            "fortune 500", "fortune global 500", "global 2000", "forbes global 2000",
            "multinational corporation", "multinational company", "large conglomerate",
            "global conglomerate", "conglomerate",
        )
        if any(marker in text for marker in explicit_markers):
            return True, None

        parent_match = re.search(
            r"(?:subsidiary|parent company|parent group|part of)\D{0,120}([A-Z][A-Za-z0-9&.,' -]{2,100})",
            text,
        )
        parent_company = parent_match.group(1).strip(" .,-") if parent_match else None
        return False, parent_company

    @classmethod
    def _build_result(
        cls,
        candidate: dict,
        evidence: list[EvidenceItem],
        combined: str,
        request: CompanyResearchRequest,
        actual_industry: str | None,
        industry_reason: str,
    ) -> CompanySearchResult:
        signals = {
            "hiring": any(k in combined for k in ("hiring", "careers", "job opening", "vacancy", "recruiting")),
            "growth": any(k in combined for k in ("expansion", "expanded", "acquisition", "funding", "investment", "new location", "growth")),
            "technology": any(k in combined for k in ("cloud", "azure", "software", "technology", "digital", "data", "erp", "crm", "modernization", "migration")),
            "ai": any(k in combined for k in ("artificial intelligence", "generative ai", "machine learning", "ai ", "automation", "copilot")),
            "process": any(k in combined for k in ("manual process", "workflow", "documents", "reporting", "compliance", "operations", "integration")),
            "funding": any(k in combined for k in ("funding", "investment", "raised", "series a", "series b", "grant")),
        }
        confirmed = [key for key, value in signals.items() if value]
        has_evidence = bool(evidence) and bool(confirmed)
        classification = "Strong opportunity signal" if has_evidence else "Reasonable business hypothesis"
        evidence_text = (
            f"Public sources show company-specific signals related to {', '.join(confirmed)}. "
            "These signals support further qualification but do not prove an active buying requirement."
            if has_evidence else
            "No reliable public evidence was found for a specific technology requirement; the opportunity below is a hypothesis for human validation."
        )

        opportunities: list[str] = []
        services: list[str] = []
        if signals["ai"]:
            opportunities.append("AI / Generative AI")
            services.append("AI Consulting")
        if signals["process"]:
            opportunities.append("Workflow / Process Improvement")
            services.append("Business Process Automation")
        if signals["technology"]:
            opportunities.append("Cloud / Software Modernization")
            services.extend(["Custom Application Development", "Azure Modernization", "Architecture Review"])
        if not opportunities:
            opportunities.append("Technology modernization")
            services.extend(["Architecture Review", "Custom Application Development"])
        services = list(dict.fromkeys(services))

        problem = (
            "Public signals suggest there may be an opportunity to improve one or more technology, workflow, data, or reporting processes."
            if has_evidence else
            "A reasonable starting hypothesis is that the company may have room to improve an internal system, workflow, integration, or reporting process; this is not a confirmed requirement."
        )
        impact = "Potential impact includes reduced manual effort, faster processing or reporting, improved integration, and better scalability."

        business_fit = 23 if request.services and any(
            cls._service_matches_requested(service, request.services) for service in services
        ) else 14
        evidence_score = 22 if has_evidence else 7
        buying_signal = 17 if (signals["hiring"] or signals["growth"] or signals["funding"]) else 6
        ability = 12 if any(
            marker in combined for marker in ("enterprise", "employees", "revenue", "funding", "investment", "million", "billion")
        ) else 7 if any(marker in combined for marker in ("established", "global company", "large company")) else 4
        accessibility = 9 if candidate["website"] else 4
        score = min(100, business_fit + evidence_score + buying_signal + ability + accessibility)
        tier = "Tier A" if score >= 80 else "Tier B" if score >= 60 else "Tier C" if score >= 40 else "Not qualified"

        role = cls._select_buyer_role(request, services, signals)
        evidence_date = next((item.evidence_date for item in evidence if item.evidence_date), None)
        observation = cls._best_observation(evidence, confirmed)
        message = (
            f"Subject: A possible improvement opportunity at {candidate['company_name']}\n\n"
            f"Hello,\n\nI was reviewing public information about {candidate['company_name']} and noticed {observation}. "
            f"We help businesses with {', '.join(services[:2])}. There may be a practical opportunity to improve a related process or technology capability. "
            "If useful, I can share a short view of what we found and where there may be a fit. Would that be worth a brief discussion?\n\nRegards"
        )

        confidence = "High" if len(evidence) >= 5 and has_evidence and industry_reason else "Medium" if evidence else "Low"
        return CompanySearchResult(
            company_name=candidate["company_name"],
            industry=actual_industry,
            industry_match=True,
            industry_match_reason=industry_reason,
            location=cls._extract_location(combined, request.geography),
            website=candidate["website"],
            company_size=cls._company_size_label(candidate.get("employee_count")),
            employee_count=candidate.get("employee_count"),
            parent_company=candidate.get("parent_company"),
            icp_match=True,
            icp_match_reason=candidate.get("icp_match_reason"),
            business_description=cls._business_description(evidence, candidate["company_name"]),
            opportunity_type=opportunities,
            evidence_of_need=evidence_text,
            evidence_classification=classification,
            business_problem_hypothesis=problem,
            recommended_solution=services,
            expected_business_impact=impact,
            trigger_event=cls._trigger_event(signals),
            evidence_date=evidence_date,
            decision_maker_role=role,
            decision_maker_name=None,
            public_contact_channel=candidate["website"],
            discovery_metadata=candidate.get("discovery_metadata", []),
            qualification_score=score,
            priority_tier=tier,
            recommended_outreach_angle=(
                f"Because {observation}, {candidate['company_name']} may be worth reviewing for a focused {services[0].lower()} opportunity."
            ),
            suggested_first_message=message,
            sources=evidence,
            confidence_level=confidence,
        )

    @staticmethod
    def _company_size_label(employee_count: int | None) -> str | None:
        if employee_count is None:
            return None
        if employee_count <= 20:
            return "Startup / Micro"
        if employee_count <= 50:
            return "Small"
        if employee_count <= 200:
            return "51-200"
        if employee_count <= 500:
            return "201-500"
        return "500+"

    @classmethod
    def _industry_match(cls, industry: str | None, text: str, targets: list[str]) -> tuple[bool, str]:
        if not targets:
            return True, "No industry restriction was requested."
        normalized_targets = [t.lower().strip() for t in targets]
        normalized_industry = (industry or "").lower()
        for target in normalized_targets:
            key = target
            if normalized_industry and (key in normalized_industry or normalized_industry in key):
                return True, f"Primary industry is consistent with requested industry: {target}."
            keywords = cls._INDUSTRY_KEYWORDS.get(key, (key,))
            positive = sum(1 for word in keywords if word in text)
            negative = sum(1 for word in cls._NEGATIVE_SERVICE_MARKERS if word in text)
            if positive >= 2 and positive > negative:
                return True, f"Public company information contains multiple signals consistent with {target}."
        return False, "Public information does not sufficiently support the requested industry."

    @classmethod
    def _infer_industry(cls, text: str, title: str, targets: list[str]) -> str | None:
        haystack = f"{title} {text}".lower()
        best_target = None
        best_score = 0
        for target in targets or cls._INDUSTRY_KEYWORDS.keys():
            keywords = cls._INDUSTRY_KEYWORDS.get(target.lower(), (target.lower(),))
            score = sum(1 for word in keywords if word in haystack)
            if score > best_score:
                best_score = score
                best_target = target
        return best_target if best_score else None

    @staticmethod
    def _business_description(evidence: list[EvidenceItem], company_name: str) -> str | None:
        for item in evidence:
            snippet = (item.snippet or "").strip()
            if snippet and company_name.lower() in snippet.lower():
                return snippet[:500]
        return None

    @staticmethod
    def _best_observation(evidence: list[EvidenceItem], signals: list[str]) -> str:
        for item in evidence:
            snippet = (item.snippet or "").strip()
            if snippet:
                clean = " ".join(snippet.split())
                return clean[:240].rstrip(".,")
        return f"public information shows signals related to {', '.join(signals) if signals else 'technology or business improvement'}"

    @staticmethod
    def _verified_official_website(name: str, candidate_website: str, items: list[dict]) -> str | None:
        """Prefer a domain that clearly matches the company name; otherwise keep the candidate only when it is a company-like domain."""
        tokens = [token for token in name.lower().replace("&", " ").split() if len(token) > 2]
        candidates: list[str] = []
        for item in items:
            url = str(item.get("url", "")).strip()
            if not url:
                continue
            domain = urlparse(url).netloc.lower().removeprefix("www.")
            if any(token in domain for token in tokens):
                candidates.append(f"{urlparse(url).scheme}://{domain}")
        if candidates:
            return candidates[0]
        parsed = urlparse(candidate_website)
        domain = parsed.netloc.lower().removeprefix("www.")
        if domain and any(token in domain for token in tokens):
            return candidate_website
        return None

    @staticmethod
    def _extract_location(text: str, fallback: str | None = None) -> str | None:
        markers = ("headquartered in ", "headquarters in ", "based in ")
        lower = text.lower()
        for marker in markers:
            idx = lower.find(marker)
            if idx >= 0:
                value = text[idx + len(marker):].split(".")[0].strip()
                if 2 <= len(value) <= 100:
                    return value.title()
        return fallback

    @staticmethod
    def _trigger_event(signals: dict[str, bool]) -> str | None:
        events = []
        if signals["hiring"]:
            events.append("technology hiring")
        if signals["growth"]:
            events.append("growth / expansion")
        if signals["funding"]:
            events.append("funding / investment")
        return ", ".join(events) if events else None

    @staticmethod
    def _service_matches_requested(service: str, requested: list[str]) -> bool:
        value = service.lower()
        aliases = {
            "azure modernization": ("azure", "modernization", "migration"),
            "custom application development": ("application", "software", "development"),
            "business process automation": ("automation", "workflow", "process"),
            "ai consulting": ("ai", "artificial intelligence"),
            "architecture review": ("architecture", "modernization", "cloud"),
        }
        return any(
            service.lower() in requested_service.lower()
            or requested_service.lower() in service.lower()
            or any(alias in requested_service.lower() for alias in aliases.get(service.lower(), ()))
            for requested_service in requested
        )

    @staticmethod
    def _select_buyer_role(request: CompanyResearchRequest, services: list[str], signals: dict[str, bool]) -> str | None:
        preferred = [x for x in request.preferred_decision_makers]
        if preferred:
            for role in preferred:
                upper = role.upper()
                if "CTO" in upper or "CIO" in upper or "COO" in upper:
                    return role
            return preferred[0]
        if "Business Process Automation" in services:
            return "COO / Operations Leader"
        if "Azure Modernization" in services or "Custom Application Development" in services:
            return "CTO / CIO"
        return "CTO / CIO / COO"

    @classmethod
    def _looks_like_article_title(cls, title: str) -> bool:
        normalized = " ".join(title.lower().split())
        if any(normalized.startswith(marker) for marker in cls._GENERIC_TITLE_MARKERS):
            return True
        if len(normalized) > 110 and any(token in normalized for token in ("companies", "manufacturing", "digital transformation")):
            return True
        return False

    @classmethod
    def _candidate_name(cls, title: str, domain: str) -> str:
        host = domain.split(".")[0].replace("-", " ").strip()
        cleaned = title.strip()
        if " | " in cleaned:
            cleaned = cleaned.split(" | ", 1)[0].strip()
        if " - " in cleaned:
            cleaned = cleaned.split(" - ", 1)[0].strip()
        lowered = f" {cleaned.lower()} "
        action_title = any(marker in lowered for marker in (
            " collaborates ", " announces ", " partners with ", " selects ",
            " launches ", " unveils ", " acquires ", " joins ", " to deliver ",
        ))
        if not cleaned or len(cleaned.split()) > 8 or action_title or cls._looks_like_article_title(cleaned):
            cleaned = host.title()
        return cleaned

    @staticmethod
    def _blocked_domain(domain: str) -> bool:
        domain = domain.lower().removeprefix("www.")
        blocked = (
            "wikipedia.org", "linkedin.com", "facebook.com", "youtube.com",
            "twitter.com", "x.com", "instagram.com", "indiamart.com",
            "tradeindia.com", "justdial.com", "sulekha.com",
        )
        return any(domain == item or domain.endswith("." + item) for item in blocked)

    @staticmethod
    def _root_url(url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"
