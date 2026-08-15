# AiSDR — Clean Replacement Baseline

This package is the cleaned replacement baseline for the AiSDR project.

## What was cleaned

- Removed the obsolete parallel ORM/model tree that defined duplicate `leads`, `contacts`, and `recommendations` tables.
- Removed the older service/repository/pipeline/automation/outreach/email/discovery implementations that were outside the current DDD/application/persistence/presentation path.
- Removed duplicate/backup presentation and dependency-injection files.
- Kept one SQLAlchemy metadata registry under `app.infrastructure.persistence.database.base.Base`.
- Kept the revised asymmetric company-discovery funnel under `app.domain.company_research.services.discovery_funnel`.
- Corrected stale imports and tests to match the current UUID-based domain contracts and repository interfaces.
- Added a reproducible dependency manifest and local environment template.

## Canonical runtime path

```text
HTTP / presentation
        ↓
Application commands / queries / handlers
        ↓
Domain entities / value objects
        ↓
Unit of Work + repository contracts
        ↓
Infrastructure persistence
        ↓
One SQLAlchemy Base.metadata registry
```

Company research intentionally remains a research-only boundary:

```text
Tavily / public discovery
        ↓
Candidate extraction
        ↓
Canonical normalization
        ↓
Deterministic hard gate
        ↓
ICP verification gate
        ↓
Deep research
        ↓
Qualification signals
```

It does not directly create CRM records.

## Local setup

Use Python 3.13 for the validated environment.

### 1. Replace the old project

Back up the existing folder, then replace it with the contents of this package. Do not merge folders manually; the cleanup intentionally removes obsolete trees.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment

```powershell
Copy-Item .env.example .env
```

or:

```bash
cp .env.example .env
```

Set `TAVILY_API_KEY` when live company discovery is required. The rest of the application can be started without a Tavily key.

### 5. Create/update the database

```bash
alembic upgrade head
```

The default local database is `aisdr.db`. It is intentionally ignored by Git.

### 6. Run tests

```bash
pytest -q
```

### 7. Start the API

```bash
uvicorn main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

## Useful verification commands

```bash
alembic heads
alembic current
alembic check
python -m compileall -q app tests
```

There should be one Alembic head: `2b97194cc80f`.

The persistence layer should expose one SQLAlchemy metadata registry and no duplicate table definitions.
