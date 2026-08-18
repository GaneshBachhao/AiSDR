import type { components } from '../api/schema';

/** qualification_router.py now declares response_model= on every route
 * (fixed 2026-08-18, see Backend IS-3 in
 * AiSDR/docs/intermediate_sprint_no_api_quota.md) -- these are real
 * generated types now, not hand-transcribed ones.
 *
 * GetQualificationResponseDTO is the canonical single-record shape (get,
 * create, update all return the identical fields). ListQualificationResponseDTO
 * is genuinely narrower -- it omits `recommendation` entirely (confirmed
 * by reading qualification_mapper.py's to_list_response), so it gets its
 * own alias rather than being folded into the single-record type. */
export type QualificationResponseDTO = components['schemas']['GetQualificationResponseDTO'];
export type QualificationListItemDTO = components['schemas']['ListQualificationResponseDTO'];
export type CreateQualificationRequestDTO = components['schemas']['CreateQualificationRequestDTO'];
export type UpdateQualificationRequestDTO = components['schemas']['UpdateQualificationRequestDTO'];

/** Transcribed from
 * Backend/app/domain/qualification/enums/qualification_status.py --
 * not an OpenAPI enum, same situation as DiscoveryStatus/AssessmentStatus.
 * A new Qualification always starts as "Partially Qualified" with score 0
 * unless status/score are passed explicitly on create
 * (Qualification.__init__ hardcodes that default; the create handler
 * only overrides it if the request included a value). */
export const QUALIFICATION_STATUSES = [
  'Qualified',
  'Partially Qualified',
  'Needs Nurturing',
  'Disqualified',
] as const;
export type QualificationStatus = (typeof QUALIFICATION_STATUSES)[number];

export function emptyQualificationForm(
  leadId = '',
  assessmentId = '',
): CreateQualificationRequestDTO {
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
