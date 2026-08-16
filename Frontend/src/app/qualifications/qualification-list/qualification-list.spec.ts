import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { QualificationList } from './qualification-list';
import { QualificationResponseDTO } from '../qualification.models';
import { AssessmentResponseDTO } from '../../assessments/assessment.models';
import { DiscoveryResponseDTO } from '../../discoveries/discovery.models';
import { LeadResponseDTO } from '../../leads/lead.models';
import { CompanyResponseDTO } from '../../companies/company.models';
import { ContactResponseDTO } from '../../contacts/contact.models';

describe('QualificationList', () => {
  let httpMock: HttpTestingController;
  const base = environment.apiBaseUrl;

  const qualifications: QualificationResponseDTO[] = [
    {
      qualification_id: 'q1',
      lead_id: 'l1',
      assessment_id: 'a1',
      status: 'Qualified',
      score: 88,
      recommendation: 'Proceed to outreach.',
    },
  ];
  const leads: LeadResponseDTO[] = [
    {
      id: 'l1',
      company_id: 'c1',
      contact_id: 'ct1',
      source: 'Other',
      status: 'New',
      score: 0,
      notes: null,
      is_qualified: false,
    },
  ];
  const companies: CompanyResponseDTO[] = [
    {
      id: 'c1',
      name: 'Acme Manufacturing',
      website: null,
      industry: null,
      company_size: null,
      employee_count: null,
      country: null,
      state: null,
      city: null,
      is_active: true,
    },
  ];
  const contacts: ContactResponseDTO[] = [
    {
      id: 'ct1',
      company_id: 'c1',
      first_name: 'Jane',
      last_name: 'Doe',
      email: 'jane@acme.example',
      phone: null,
      job_title: null,
      linkedin_url: null,
      is_active: true,
    },
  ];
  const assessments: AssessmentResponseDTO[] = [
    {
      assessment_id: 'a1',
      discovery_id: 'd1',
      status: 'Completed',
      summary: null,
      maturity_level: 'Defined',
      readiness_score: 80,
      strengths: null,
      weaknesses: null,
      opportunities: null,
      risks: null,
    },
  ];
  const discoveries: DiscoveryResponseDTO[] = [
    {
      id: 'd1',
      lead_id: 'l1',
      problem_statement: 'Manual monthly reporting.',
      current_solution: null,
      business_impact: null,
      success_criteria: null,
      status: 'COMPLETED',
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QualificationList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('renders the resolved lead and assessment labels, score, and status badge', async () => {
    const fixture = TestBed.createComponent(QualificationList);
    fixture.detectChanges();

    httpMock.expectOne(`${base}/qualifications?skip=0&limit=200`).flush(qualifications);
    httpMock.expectOne(`${base}/leads?limit=500`).flush(leads);
    httpMock.expectOne(`${base}/companies?limit=500`).flush(companies);
    httpMock.expectOne(`${base}/contacts?limit=500`).flush(contacts);
    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush(assessments);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush(discoveries);
    await fixture.whenStable();
    fixture.detectChanges();

    const row = fixture.nativeElement.querySelector('tbody tr');
    expect(row.textContent).toContain('Acme Manufacturing — Jane Doe');
    expect(row.textContent).toContain('Manual monthly reporting.');
    expect(row.textContent).toContain('88');
    const badge = row.querySelector('.badge');
    expect(badge.classList).toContain('badge-ok');
    expect(badge.textContent).toContain('Qualified');
  });
});
