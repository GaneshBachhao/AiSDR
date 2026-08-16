import type { components } from '../api/schema';

export type DiscoveryResponseDTO = components['schemas']['DiscoveryResponseDTO'];
export type CreateDiscoveryRequestDTO = components['schemas']['CreateDiscoveryRequestDTO'];
export type UpdateDiscoveryRequestDTO = components['schemas']['UpdateDiscoveryRequestDTO'];

/** The schema types `status` as a bare `string` (FastAPI didn't expose
 * DiscoveryStatus as an OpenAPI enum the way it did LeadStatus/LeadSource),
 * so this list is transcribed directly from
 * Backend/app/domain/discovery/enums/discovery_status.py rather than
 * generated -- keep it in sync by hand if that enum changes. */
export const DISCOVERY_STATUSES = ['CREATED', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED', 'CANCELLED'] as const;
export type DiscoveryStatus = (typeof DISCOVERY_STATUSES)[number];

const NEEDS_FIELDS = ['problem_statement', 'current_solution', 'business_impact', 'success_criteria'] as const;

export function emptyDiscoveryForm(leadId = ''): CreateDiscoveryRequestDTO {
  return {
    lead_id: leadId,
    problem_statement: null,
    current_solution: null,
    business_impact: null,
    success_criteria: null,
  };
}

/** How many of the 4 optional discovery-needs fields are actually
 * captured -- every field on Create/UpdateDiscoveryRequestDTO is
 * optional, and live data shows most records only have 1 of 4 filled, so
 * the UI should say so honestly rather than imply a record is "complete"
 * just because it exists. */
export function discoveryCompleteness(discovery: DiscoveryResponseDTO): { filled: number; total: number } {
  const filled = NEEDS_FIELDS.filter((field) => !!discovery[field]?.trim()).length;
  return { filled, total: NEEDS_FIELDS.length };
}

export function discoveryStatusBadgeClass(status: string): string {
  switch (status) {
    case 'COMPLETED':
      return 'badge-ok';
    case 'CANCELLED':
      return 'badge-fail';
    case 'IN_PROGRESS':
      return 'badge-warn';
    case 'CREATED':
      return 'badge-info';
    case 'ON_HOLD':
    default:
      return 'badge-neutral';
  }
}
