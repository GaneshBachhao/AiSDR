/**
 * Type aliases onto the OpenAPI-generated schema (EPIC-F02) -- these used
 * to be hand-written interfaces, verified field-for-field against a live
 * `/openapi.json` snapshot. Now they *are* generated, via
 * `npm run generate:api` (see package.json / Frontend/README.md), so
 * drift is no longer possible to miss silently.
 */

import type { components } from '../api/schema';

export type CompanyResearchRequest = components['schemas']['CompanyResearchRequest'];
export type EvidenceItem = components['schemas']['EvidenceItem'];
export type DiscoveredContact = components['schemas']['DiscoveredContact'];
export type DiscoverySourceMetadata = components['schemas']['DiscoverySourceMetadata'];
export type CompanySearchResult = components['schemas']['CompanySearchResult'];
export type CandidateResearchFailure = components['schemas']['CandidateResearchFailure'];
export type CompanyResearchBatchResult = components['schemas']['CompanyResearchBatchResult'];

export function defaultCompanyResearchRequest(): CompanyResearchRequest {
  return {
    industries: [],
    geography: '',
    company_size: [],
    revenue_range: null,
    technologies: [],
    services: [],
    ideal_customer_profile: null,
    number_of_companies: 10,
    research_period: 'last 6 months',
    minimum_qualification_score: 0,
    preferred_decision_makers: [],
    target_language: 'English',
    persist_as_companies: false,
  };
}
