/**
 * Mirrors app/application/company_research/dto/company_research_request.py
 * and company_research_response.py in the AiSDR backend. Kept as plain
 * interfaces (not generated) for this first vertical slice -- see the
 * frontend README for the tradeoff and the plan to move to OpenAPI-generated
 * types once the pattern proves out across more than one module.
 */

export interface CompanyResearchRequest {
  industries: string[];
  geography: string;
  company_size: string[];
  revenue_range?: string | null;
  technologies: string[];
  services: string[];
  ideal_customer_profile?: string | null;
  number_of_companies: number;
  research_period: string;
  minimum_qualification_score: number;
  preferred_decision_makers: string[];
  target_language: string;
  persist_as_companies: boolean;
}

export interface EvidenceItem {
  title: string;
  url: string;
  snippet?: string | null;
  evidence_date?: string | null;
  observed_date?: string | null;
  signal_scope: 'company_specific' | 'industry_general';
}

export interface DiscoveredContact {
  name: string;
  role_title?: string | null;
  linkedin_url?: string | null;
  source_url?: string | null;
  email?: string | null;
}

export interface DiscoverySourceMetadata {
  source_type: string;
  source_title: string;
  source_url: string;
  discovered_record_count?: number | null;
  metadata_observed_at?: string | null;
}

export interface CompanySearchResult {
  company_name: string;
  industry?: string | null;
  industry_match: boolean;
  industry_match_reason?: string | null;
  location?: string | null;
  website?: string | null;
  company_size?: string | null;
  employee_count?: number | null;
  parent_company?: string | null;
  icp_match: boolean;
  icp_match_reason?: string | null;
  business_description?: string | null;
  opportunity_type: string[];
  evidence_of_need: string;
  evidence_classification: string;
  business_problem_hypothesis: string;
  recommended_solution: string[];
  expected_business_impact: string;
  trigger_event?: string | null;
  evidence_date?: string | null;
  decision_maker_role?: string | null;
  decision_maker_name?: string | null;
  public_contact_channel?: string | null;
  discovered_contacts: DiscoveredContact[];
  discovery_metadata: DiscoverySourceMetadata[];
  qualification_score: number;
  priority_tier: string;
  recommended_outreach_angle: string;
  suggested_first_message: string;
  sources: EvidenceItem[];
  confidence_level: string;
  source: string;
  persisted_company_id?: string | null;
  persisted_contact_id?: string | null;
  persisted_lead_id?: string | null;
  lead_creation_skipped_reason?: string | null;
}

export interface CandidateResearchFailure {
  company_name: string;
  website?: string | null;
  title: string;
  content: string;
  source_url: string;
  discovery_metadata: DiscoverySourceMetadata[];
  failed_step: string;
  error_message: string;
  is_resumable: boolean;
}

export interface CompanyResearchBatchResult {
  results: CompanySearchResult[];
  failures: CandidateResearchFailure[];
}

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
