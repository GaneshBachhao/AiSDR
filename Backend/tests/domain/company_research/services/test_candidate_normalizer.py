from app.domain.company_research.entities.candidate import CompanyCandidate
from app.domain.company_research.services.candidate_normalizer import CandidateNormalizer


def test_normalize_name_strips_punctuation_and_case():
    assert CandidateNormalizer.normalize_name("ABC Pvt. Ltd.") == "abc pvt ltd"
    assert CandidateNormalizer.normalize_name("ABC PRIVATE LIMITED") == "abc private limited"


def test_normalize_root_url_strips_www_path_and_query():
    assert (
        CandidateNormalizer.normalize_root_url("https://www.acme.example/about?x=1") == "https://acme.example"
    )


def test_normalize_root_url_returns_none_for_missing_or_invalid_value():
    assert CandidateNormalizer.normalize_root_url(None) is None
    assert CandidateNormalizer.normalize_root_url("not-a-url") is None


def test_canonical_key_prefers_domain_over_name():
    candidate = CompanyCandidate(
        company_name="Acme Manufacturing",
        website="https://www.acme.example",
        title="Acme Manufacturing",
        content="",
        source_url="https://www.acme.example",
    )
    assert CandidateNormalizer.canonical_key(candidate) == "domain:acme.example"


def test_canonical_key_falls_back_to_normalized_name_without_website():
    candidate = CompanyCandidate(
        company_name="Acme Manufacturing",
        website=None,
        title="Acme Manufacturing",
        content="",
        source_url="https://acme.example/result",
    )
    assert CandidateNormalizer.canonical_key(candidate) == "name:acme manufacturing"
