import type { components } from '../api/schema';

export type RecommendationResponseDTO = components['schemas']['RecommendationDTO'];
export type GenerateRecommendationRequestDTO = components['schemas']['GenerateRecommendationRequest'];
export type SolutionSummaryDTO = components['schemas']['SolutionSummaryDTO'];

/** Like DiscoveryStatus/AssessmentStatus, RecommendationStatus isn't
 * exposed as an OpenAPI enum -- transcribed from
 * Backend/app/domain/recommendation/enums/recommendation_status.py by
 * hand. Note the gap this reflects: Submit/Approve application handlers
 * exist server-side but, like the old company_research funnel, were never
 * wired into recommendation_router.py -- only Draft is actually reachable
 * through the API today (verified by reading the router directly, not
 * just the generated schema). The other four values are listed for
 * completeness/future-proofing, not because this frontend can drive a
 * transition to them. */
export const RECOMMENDATION_STATUSES = [
  'Draft',
  'Under Review',
  'Approved',
  'Rejected',
  'Archived',
] as const;
export type RecommendationStatus = (typeof RECOMMENDATION_STATUSES)[number];

export function recommendationStatusBadgeClass(status: string): string {
  switch (status) {
    case 'Approved':
      return 'badge-ok';
    case 'Rejected':
      return 'badge-fail';
    case 'Under Review':
      return 'badge-warn';
    case 'Draft':
      return 'badge-info';
    case 'Archived':
    default:
      return 'badge-neutral';
  }
}
