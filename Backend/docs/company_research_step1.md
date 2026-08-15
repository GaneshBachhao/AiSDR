# Step 1 — Company Research

This step adds an isolated public-web company research endpoint.

## Endpoint

`POST /company-research/search`

It discovers companies and returns research candidates. It does not create or modify:

- Company
- Contact
- Lead
- Discovery
- Assessment
- Qualification
- Recommendation

It also does not send outreach.

## Inputs

The request supports industries, geography, company size, revenue range, technologies, services, ICP, company count, research period, minimum score, preferred decision-maker roles, and language.

## Research rules

- Public-web evidence is preferred.
- Evidence is kept separate from assumptions.
- When reliable evidence is not found, the result explicitly says so and provides a clearly labelled business problem hypothesis.
- Service recommendations are broader than AI/automation and can include custom application development, Azure modernization, Azure migration, architecture review, integration, data modernization, and related services.
- Decision-maker names are not invented.
- Output is intended to be reviewed by a human before CRM creation or outreach.

## Configuration

The endpoint uses the project's existing Tavily integration. Keep the existing `.env` file in place and configure `TAVILY_API_KEY` there.

The provided replacement ZIP does not contain the project's `.env` or local `aisdr.db`; keep those from your current installation.
