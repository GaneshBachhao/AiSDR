import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { CompanyDetail } from './company-detail';
import { CompanyResponseDTO } from '../company.models';
import { ContactResponseDTO } from '../../contacts/contact.models';
import { LeadResponseDTO } from '../../leads/lead.models';
import { DiscoveryResponseDTO } from '../../discoveries/discovery.models';

describe('CompanyDetail', () => {
  let httpMock: HttpTestingController;
  const base = environment.apiBaseUrl;

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
  const contacts: ContactResponseDTO[] = [
    {
      id: 'ct1',
      company_id: 'c1',
      first_name: 'Jane',
      last_name: 'Doe',
      email: 'jane@acme.example',
      phone: null,
      job_title: 'VP Operations',
      linkedin_url: null,
      is_active: true,
    },
    {
      id: 'ct2',
      company_id: 'c2',
      first_name: 'John',
      last_name: 'Smith',
      email: 'john@other.example',
      phone: null,
      job_title: null,
      linkedin_url: null,
      is_active: true,
    },
  ];
  const leads: LeadResponseDTO[] = [
    {
      id: 'l1',
      company_id: 'c1',
      contact_id: 'ct1',
      source: 'Other',
      status: 'Qualified',
      score: 80,
      notes: null,
      is_qualified: true,
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
      status: 'IN_PROGRESS',
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    },
    {
      id: 'd2',
      lead_id: 'l-other-company',
      problem_statement: 'Unrelated discovery for a different company.',
      current_solution: null,
      business_impact: null,
      success_criteria: null,
      status: 'CREATED',
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CompanyDetail],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: new Map([['id', 'c1']]) } } },
      ],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('surfaces the company real Contacts, Leads, and Discoveries with cross-links', async () => {
    const fixture = TestBed.createComponent(CompanyDetail);
    fixture.detectChanges();

    httpMock.expectOne(`${base}/companies/c1`).flush(company);
    await fixture.whenStable();
    fixture.detectChanges();

    httpMock.expectOne(`${base}/contacts?limit=500`).flush(contacts);
    httpMock.expectOne(`${base}/leads?company_id=c1&limit=500`).flush(leads);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush(discoveries);
    await fixture.whenStable();
    fixture.detectChanges();

    const sections = fixture.nativeElement.querySelectorAll('.related');
    const [contactsSection, leadsSection, discoveriesSection] = sections;

    expect(contactsSection.textContent).toContain('Jane Doe');
    expect(contactsSection.textContent).toContain('VP Operations');
    expect(contactsSection.textContent).not.toContain('John Smith');

    expect(leadsSection.textContent).toContain('Jane Doe');
    const leadBadge = leadsSection.querySelector('.badge');
    expect(leadBadge.classList).toContain('badge-ok');
    expect(leadBadge.textContent).toContain('Qualified');

    expect(discoveriesSection.textContent).toContain('Manual monthly reporting.');
    expect(discoveriesSection.textContent).not.toContain('Unrelated discovery');
    const discoveryBadge = discoveriesSection.querySelector('.badge');
    expect(discoveryBadge.textContent).toContain('IN_PROGRESS');
  });
});
