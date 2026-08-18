import type { components } from '../api/schema';

/** The backend emits four structurally-identical response DTOs
 * (Create/Get/List/UpdateAssessmentResponseDTO) instead of one shared
 * one -- verified field-for-field identical in the generated schema, so
 * one canonical alias is used everywhere on the frontend rather than
 * juggling four names for the same shape. */
export type AssessmentResponseDTO = components['schemas']['GetAssessmentResponseDTO'];
export type CreateAssessmentRequestDTO = components['schemas']['CreateAssessmentRequestDTO'];
export type UpdateAssessmentRequestDTO = components['schemas']['UpdateAssessmentRequestDTO'];

/** Like DiscoveryStatus, AssessmentStatus/MaturityLevel aren't exposed as
 * OpenAPI enums -- transcribed from
 * Backend/app/domain/assessment/enums/{assessment_status,maturity_level}.py
 * by hand; keep in sync manually if those change. */
export const ASSESSMENT_STATUSES = [
  'Created',
  'In Progress',
  'Under Review',
  'Completed',
  'Cancelled',
] as const;
export type AssessmentStatus = (typeof ASSESSMENT_STATUSES)[number];

export const MATURITY_LEVELS = [
  'Initial',
  'Developing',
  'Defined',
  'Managed',
  'Optimized',
] as const;
export type MaturityLevel = (typeof MATURITY_LEVELS)[number];

export function assessmentStatusBadgeClass(status: string): string {
  switch (status) {
    case 'Completed':
      return 'badge-ok';
    case 'Cancelled':
      return 'badge-fail';
    case 'In Progress':
    case 'Under Review':
      return 'badge-warn';
    case 'Created':
      return 'badge-info';
    default:
      return 'badge-neutral';
  }
}
