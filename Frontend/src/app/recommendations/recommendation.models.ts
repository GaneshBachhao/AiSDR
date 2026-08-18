import type { components } from '../api/schema';

export type RecommendationResponseDTO = components['schemas']['RecommendationDTO'];
export type GenerateRecommendationRequestDTO =
  components['schemas']['GenerateRecommendationRequest'];
export type SolutionSummaryDTO = components['schemas']['SolutionSummaryDTO'];

/** Like DiscoveryStatus/AssessmentStatus, RecommendationStatus isn't
 * exposed as an OpenAPI enum -- transcribed from
 * Backend/app/domain/recommendation/enums/recommendation_status.py by
 * hand. Draft -> Under Review -> Approved are reachable from this
 * frontend via RecommendationService.submit()/approve() (IS-4/IS-8);
 * Rejected/Archived have no application handler wired to any endpoint
 * yet, so no UI drives a transition to them. */
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
