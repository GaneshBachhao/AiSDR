Company Research Discovery v3 — Ready to Replace

Purpose
- Treat generic directory/search pages as discovery sources, not company records.
- Extract real company candidates from directory snippets when available.
- Preserve dynamic discovery metadata observed on each run.
- The record count/title is parsed from the live result; nothing is hard-coded to 13,284,167.
- Expand the candidate pool before qualification so the requested Top-N can be filled from genuinely qualified companies.

Dynamic metadata example
- source_title: whatever title the search result has on that run
- discovered_record_count: parsed record count when present, otherwise null
- source_url: the discovery page URL
- metadata_observed_at: UTC observation timestamp

Important
The discovery record count is source metadata only. It does not contribute directly to the company qualification score.
