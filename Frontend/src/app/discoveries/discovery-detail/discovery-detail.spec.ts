import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { DiscoveryDetail } from './discovery-detail';
import { DiscoveryResponseDTO } from '../discovery.models';
import { LeadResponseDTO } from '../../leads/lead.models';
import { CompanyResponseDTO } from '../../companies/company.models';
import { ContactResponseDTO } from '../../contacts/contact.models';
import { AssessmentResponseDTO } from '../../assessments/assessment.models';
import { RecommendationResponseDTO } from '../../recommendations/recommendation.models';

describe('DiscoveryDetail', () => {
  let httpMock: HttpTestingController;
  const base = environment.apiBaseUrl;

  const discovery: DiscoveryResponseDTO = {
    id: 'd1',
    lead_id: 'l1',
    problem_statement: 'Manual monthly reporting.',
    current_solution: null,
    business_impact: null,
    success_criteria: null,
    status: 'IN_PROGRESS',
    created_at: '2026-08-16T00:00:00Z',
    updated_at: '2026-08-16T00:00:00Z',
  };
  const lead: LeadResponseDTO = {
    id: 'l1',
    company_id: 'c1',
    contact_id: 'ct1',
    source: 'Other',
    status: 'New',
    score: 0,
    notes: null,
    is_qualified: false,
  };
  const company: CompanyResponseDTO = {
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
  };
  const contact: ContactResponseDTO = {
    id: 'ct1',
    company_id: 'c1',
    first_name: 'Jane',
    last_name: 'Doe',
    email: 'jane@acme.example',
    phone: null,
    job_title: null,
    linkedin_url: null,
    is_active: true,
  };

  function setUp() {
    return TestBed.configureTestingModule({
      imports: [DiscoveryDetail],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: new Map([['id', 'd1']]) } } },
      ],
    }).compileComponents();
  }

  async function loadBase(fixture: ComponentFixture<DiscoveryDetail>) {
    fixture.detectChanges();
    httpMock.expectOne(`${base}/discoveries/d1`).flush(discovery);
    await fixture.whenStable();
    httpMock.expectOne(`${base}/leads/l1`).flush(lead);
    httpMock.expectOne(`${base}/companies/c1`).flush(company);
    httpMock.expectOne(`${base}/contacts/ct1`).flush(contact);
  }

  beforeEach(async () => {
    await setUp();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('offers "+ Add Assessment" when the discovery has none yet', async () => {
    const fixture = TestBed.createComponent(DiscoveryDetail);
    await loadBase(fixture);

    httpMock.expectOne(`${base}/assessments?page=1&page_size=1&discovery_id=d1`).flush([]);
    await fixture.whenStable();
    fixture.detectChanges();

    const actions = fixture.nativeElement.querySelector('.actions');
    expect(actions.textContent).toContain('+ Add Assessment');
    expect(actions.textContent).not.toContain('View Assessment');
    expect(actions.textContent).not.toContain('View Recommendation');
  });

  it('links to the existing Assessment and Recommendation instead of offering to create duplicates', async () => {
    const fixture = TestBed.createComponent(DiscoveryDetail);
    await loadBase(fixture);

    const assessment: AssessmentResponseDTO = {
      assessment_id: 'a1',
      discovery_id: 'd1',
      status: 'In Progress',
      summary: null,
      maturity_level: 'Developing',
      readiness_score: 50,
      strengths: null,
      weaknesses: null,
      opportunities: null,
      risks: null,
    };
    httpMock
      .expectOne(`${base}/assessments?page=1&page_size=1&discovery_id=d1`)
      .flush([assessment]);
    await fixture.whenStable();

    const recommendation: RecommendationResponseDTO = {
      id: 'r1',
      assessment_id: 'a1',
      status: 'Draft',
      executive_summary: null,
      submitted_at: null,
      approved_at: null,
      solutions: [],
      roadmap_phases: [],
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    };
    httpMock.expectOne(`${base}/recommendations?page=1&page_size=200`).flush([recommendation]);
    await fixture.whenStable();
    fixture.detectChanges();

    const actions = fixture.nativeElement.querySelector('.actions');
    expect(actions.textContent).not.toContain('+ Add Assessment');
    expect(actions.textContent).toContain('View Assessment (In Progress)');
    expect(actions.textContent).toContain('View Recommendation (Draft)');
  });
});
