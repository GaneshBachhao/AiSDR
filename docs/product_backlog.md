| ID     | Priority | Area     | Idea                            | Status  |
| ------ | -------- | -------- | ------------------------------- | ------- |
| PB-001 | Low      | AI       | Multi-agent debate reasoner     | Backlog |
| PB-002 | Medium   | Reports  | Interactive executive dashboard | Backlog |
| PB-003 | Low      | Workflow | BPMN export                     | Backlog |

\

| ID     | Priority | Area      | Idea                                                           |
| ------ | -------- | --------- | -------------------------------------------------------------- |
| PB-001 | Medium   | Common    | Introduce `Email`, `PhoneNumber`, `Website` value objects      |
| PB-002 | Low      | Common    | Introduce shared `Severity` and `Priority` value objects       |
| PB-003 | Low      | Common    | Introduce `BaseEnum` for common enum behavior                  |
| PB-004 | Medium   | Domain    | Make aggregate collections read-only outside aggregate methods |
| PB-005 | Low      | Discovery | Metadata-driven discovery questionnaires (YAML/DB)             |

| Rule    | Description                                                                                     |
| ------- | ----------------------------------------------------------------------------------------------- |
| INV-001 | An Assessment must belong to exactly one Discovery Session.                                     |
| INV-002 | An Assessment cannot be completed before it is started.                                         |
| INV-003 | Only an `IN_PROGRESS` assessment can receive new findings.                                      |
| INV-004 | Every Finding must belong to exactly one Assessment.                                            |
| INV-005 | Every Evidence must belong to exactly one Finding.                                              |
| INV-006 | Assessment scores must remain within the defined range (e.g., 0–100).                           |
| INV-007 | Maturity level should be consistent with the calculated score (enforced by the domain service). |

| ID         | Description                         | Status   |
| ---------- | ----------------------------------- | -------- |
| PB-001     | Email VO                            | Deferred |
| PB-002     | Severity/Priority VO                | Deferred |
| PB-003     | BaseEnum                            | Deferred |
| PB-004     | Read-only Aggregate Collections     | Deferred |
| PB-005     | Metadata Discovery                  | Deferred |
| PB-006     | ImpactAssessment VO                 | Deferred |
| PB-007     | AssessmentDimensionType Enum        | Deferred |
| PB-008     | Common Scoring Framework            | Deferred |
| **PB-009** | Prevent completion without findings | Deferred |
