# Lead Rectification — ContactId model

## Business model locked

Lead belongs to a Company/Account and references a Contact by `contact_id`.

Lead does **not** duplicate Contact-owned data such as:

- contact_name
- email
- phone
- website

Lead owns:

- company_id
- contact_id
- source
- status
- score
- notes
- is_qualified

## Required relationship rule

On create and when changing `contact_id`, the application verifies that the
Contact exists and belongs to the Lead Company/Account.

## Included replacement files

- Lead domain aggregate
- Lead application commands/queries/DTOs/mapper/validator
- Lead application handlers
- Lead repository contract
- Lead persistence model/mapper/repository
- Lead API router
- Legacy Lead request/response schemas aligned to the same model
- Alembic migration from the prior Lead schema

## Not replaced

The following remain unchanged because the current project wiring already
supports the Lead handlers:

- `app/application/common/interfaces/unit_of_work.py`
- `app/infrastructure/persistence/unit_of_work/sqlalchemy_unit_of_work.py`
- `app/presentation/api/dependencies/handlers.py`

## Migration

Migration:
`f2c7e1a9b4d6_lead_contact_reference_model.py`

It preserves the existing `contact_id` relationship, adds Lead-owned source,
score, notes, and qualification fields, and removes duplicated Contact fields.

If existing Lead rows have NULL `contact_id`, migration stops intentionally.
Those rows must be associated with real Contacts before the column can be
made required.
