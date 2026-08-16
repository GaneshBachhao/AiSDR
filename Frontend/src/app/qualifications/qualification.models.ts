/**
 * Unlike every prior module, `qualification_router.py` has no
 * `response_model=` on any route (verified directly in
 * Backend/app/presentation/api/routers/qualification_router.py), so
 * `openapi-typescript` emits `unknown` for every response body here --
 * there's no generated schema to alias onto. Hand-written instead, from
 * the real DTOs in
 * Backend/app/application/qualification/dto/qualification_response.py,
 * the same manual-sync discipline already used for DiscoveryStatus/
 * AssessmentStatus. A real fix would be adding response_model= server-side
 * (a backend change, out of scope here -- see frontend_backlog.md
 * EPIC-F02's "surfaced, not fixed" note, which first flagged this gap).
 */
export interface QualificationResponseDTO {
  qualification_id: string;
  lead_id: string;
  assessment_id: string;
  status: string;
  score: number;
  recommendation: string | null;
}

export interface CreateQualificationRequestDTO {
  lead_id: string;
  assessment_id: string;
  status?: string | null;
  score?: number | null;
  recommendation?: string | null;
}

export interface UpdateQualificationRequestDTO {
  status?: string | null;
  score?: number | null;
  recommendation?: string | null;
}

/** Transcribed from
 * Backend/app/domain/qualification/enums/qualification_status.py --
 * also not an OpenAPI enum, same situation as DiscoveryStatus/
 * AssessmentStatus. A new Qualification always starts as "Partially
 * Qualified" with score 0 unless status/score are passed explicitly on
 * create (Qualification.__init__ hardcodes that default; the create
 * handler only overrides it if the request included a value). */
export const QUALIFICATION_STATUSES = [
  'Qualified',
  'Partially Qualified',
  'Needs Nurturing',
  'Disqualified',
] as const;
export type QualificationStatus = (typeof QUALIFICATION_STATUSES)[number];

export function emptyQualificationForm(leadId = '', assessmentId = ''): CreateQualificationRequestDTO {
  return {
    lead_id: leadId,
    assessment_id: assessmentId,
    status: 'Partially Qualified',
    score: 0,
    recommendation: null,
  };
}

export function qualificationStatusBadgeClass(status: string): string {
  switch (status) {
    case 'Qualified':
      return 'badge-ok';
    case 'Disqualified':
      return 'badge-fail';
    case 'Partially Qualified':
      return 'badge-warn';
    case 'Needs Nurturing':
      return 'badge-info';
    default:
      return 'badge-neutral';
  }
}
