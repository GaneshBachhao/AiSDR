from app.domain.company_research.entities.candidate import CompanyCandidate


def test_canonical_name_normalizes_case_and_whitespace():
    candidate = CompanyCandidate(
        company_name="  Acme   Manufacturing  ",
        website=None,
        title="Acme Manufacturing",
        content="",
        source_url="https://acme.example",
    )
    assert candidate.canonical_name == "acme manufacturing"


def test_canonical_domain_strips_www_and_lowercases():
    candidate = CompanyCandidate(
        company_name="Acme",
        website="https://WWW.Acme.Example/about",
        title="Acme",
        content="",
        source_url="https://acme.example",
    )
    assert candidate.canonical_domain == "acme.example"


def test_canonical_domain_is_none_without_website():
    candidate = CompanyCandidate(
        company_name="Acme",
        website=None,
        title="Acme",
        content="",
        source_url="https://acme.example/result",
    )
    assert candidate.canonical_domain is None
