from __future__ import annotations

import re

from app.domain.company_research.value_objects.domain_profile import DomainProfile

_DEFAULT_ENTERPRISE_MARKERS = (
    "fortune 500",
    "fortune global 500",
    "global 2000",
    "forbes global 2000",
    "multinational corporation",
    "multinational company",
    "large conglomerate",
    "global conglomerate",
    "conglomerate",
)


class IcpMatcher:
    """Deterministic ICP (Ideal Customer Profile) size/scale rules.

    ICP size is a hard gate: when a request specifies ``company_size``,
    an unknown employee count must never silently pass. This mirrors the
    pre-existing behavior in the discovery funnel, just relocated to a
    pure, independently testable domain service.

    ``enterprise_exclusion`` accepts an optional ``DomainProfile`` to
    override the exclusion threshold/markers per-sector. When omitted,
    behavior matches the pre-Domain-Profile defaults exactly.
    """

    @staticmethod
    def extract_employee_count(text: str) -> int | None:
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
    def size_range(value: str) -> tuple[int, int] | None:
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

    @classmethod
    def matches_size(
        cls,
        text: str,
        requested_sizes: list[str],
    ) -> tuple[bool, int | None, str]:
        """Return whether an explicit employee count satisfies the requested ICP size."""
        employee_count = cls.extract_employee_count(text)
        if not requested_sizes:
            return True, employee_count, "No company-size restriction was requested."
        if employee_count is None:
            return (
                False,
                None,
                "Employee count could not be verified; size-restricted discovery requires explicit size evidence.",
            )

        ranges = [r for r in (cls.size_range(value) for value in requested_sizes) if r is not None]
        if not ranges:
            return False, employee_count, "Requested company-size values are not recognized."
        if any(lower <= employee_count <= upper for lower, upper in ranges):
            return (
                True,
                employee_count,
                f"Verified employee count {employee_count} matches the requested company-size range.",
            )
        return (
            False,
            employee_count,
            f"Verified employee count {employee_count} is outside the requested company-size range.",
        )

    @staticmethod
    def enterprise_exclusion(
        text: str,
        employee_count: int | None,
        profile: DomainProfile | None = None,
    ) -> tuple[bool, str | None]:
        threshold = profile.enterprise_exclusion_threshold if profile is not None else 500
        explicit_markers = (
            profile.enterprise_exclusion_markers
            if profile is not None and profile.enterprise_exclusion_markers
            else _DEFAULT_ENTERPRISE_MARKERS
        )

        if employee_count is not None and employee_count > threshold:
            return True, None
        if any(marker in text for marker in explicit_markers):
            return True, None

        parent_match = re.search(
            r"(?:subsidiary|parent company|parent group|part of)\D{0,120}?([A-Z][A-Za-z0-9&.,' -]{2,100})",
            text,
        )
        parent_company = parent_match.group(1).strip(" .,-") if parent_match else None
        return False, parent_company

    @staticmethod
    def company_size_label(employee_count: int | None) -> str | None:
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
