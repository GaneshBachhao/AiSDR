import type { components } from '../api/schema';

export type CompanyResponseDTO = components['schemas']['CompanyResponseDTO'];
export type CreateCompanyRequestDTO = components['schemas']['CreateCompanyRequestDTO'];
export type UpdateCompanyRequestDTO = components['schemas']['UpdateCompanyRequestDTO'];

export function emptyCompanyForm(): CreateCompanyRequestDTO {
  return {
    name: '',
    website: null,
    industry: null,
    company_size: null,
    employee_count: null,
    country: null,
    state: null,
    city: null,
  };
}
