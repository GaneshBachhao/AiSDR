from app.company_research.funnel.candidate import DiscoveryCandidate
from app.company_research.funnel.gate import DeterministicCandidateGate
from app.company_research.funnel.pipeline import DiscoveryFunnel


def candidate(name: str, url: str, title: str | None = None) -> DiscoveryCandidate:
    return DiscoveryCandidate(
        company_name=name,
        website=url,
        title=title or name,
        content="company information",
        source_url=url,
    )


def test_gate_rejects_directory_and_social_results_before_verification():
    funnel = DiscoveryFunnel()
    accepted, metrics = funnel.gate_candidates([
        candidate("A Directory", "https://directory.example", "Top 20 Manufacturing Companies"),
        candidate("Social Page", "https://linkedin.com/company/acme"),
        candidate("Acme Manufacturing", "https://acme.example"),
    ])
    assert [item.company_name for item in accepted] == ["Acme Manufacturing"]
    assert metrics.discovered == 3
    assert metrics.deterministic_accepted == 1
    assert metrics.deterministic_rejected == 2


def test_gate_deduplicates_by_canonical_domain():
    funnel = DiscoveryFunnel()
    accepted, _ = funnel.gate_candidates([
        candidate("Acme", "https://www.acme.example/path"),
        candidate("Acme Manufacturing", "https://acme.example/about"),
    ])
    assert len(accepted) == 1


def test_gate_is_safe_for_missing_website_when_source_url_is_valid():
    gate = DeterministicCandidateGate()
    item = DiscoveryCandidate(
        company_name="Acme",
        website=None,
        title="Acme",
        content="",
        source_url="https://acme.example/result",
    )
    assert gate.evaluate(item).accepted is True


def test_gate_rejects_known_document_and_directory_domains():
    funnel = DiscoveryFunnel()
    accepted, _ = funnel.gate_candidates([
        candidate("Scribd", "https://www.scribd.com/document/123"),
        candidate("SimplyHired", "https://www.simplyhired.co.in/jobs"),
    ])
    assert accepted == []
