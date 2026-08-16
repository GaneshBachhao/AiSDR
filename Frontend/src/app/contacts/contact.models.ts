import type { components } from '../api/schema';

export type ContactResponseDTO = components['schemas']['ContactResponseDTO'];
export type CreateContactRequestDTO = components['schemas']['CreateContactRequestDTO'];
export type UpdateContactRequestDTO = components['schemas']['UpdateContactRequestDTO'];

export function emptyContactForm(companyId = ''): CreateContactRequestDTO {
  return {
    company_id: companyId,
    first_name: '',
    last_name: '',
    email: '',
    phone: null,
    job_title: null,
    linkedin_url: null,
  };
}
