import type { components } from '../api/schema';

export type LeadResponseDTO = components['schemas']['LeadResponseDTO'];
export type CreateLeadRequestDTO = components['schemas']['CreateLeadRequestDTO'];
export type UpdateLeadRequestDTO = components['schemas']['UpdateLeadRequestDTO'];
export type LeadSource = components['schemas']['LeadSource'];
export type LeadStatus = components['schemas']['LeadStatus'];

export const LEAD_SOURCES: LeadSource[] = [
  'Website',
  'Referral',
  'LinkedIn',
  'Email',
  'Phone',
  'Event',
  'Partner',
  'AI Research',
  'Other',
];

export const LEAD_STATUSES: LeadStatus[] = [
  'New',
  'Contacted',
  'Qualified',
  'Disqualified',
  'Converted',
  'Closed',
];

export function emptyLeadForm(companyId = '', contactId = ''): CreateLeadRequestDTO {
  return {
    company_id: companyId,
    contact_id: contactId,
    source: 'Other',
    score: 0,
    notes: null,
  };
}

/** Same badge vocabulary as Contact's Active/Inactive treatment, extended
 * to Lead's six-state lifecycle instead of a hardcoded single color. */
export function leadStatusBadgeClass(status: LeadStatus): string {
  switch (status) {
    case 'Qualified':
    case 'Converted':
      return 'badge-ok';
    case 'Disqualified':
      return 'badge-fail';
    case 'Contacted':
      return 'badge-warn';
    case 'New':
      return 'badge-info';
    case 'Closed':
    default:
      return 'badge-neutral';
  }
}
