import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { LeadList } from './lead-list';
import { LeadResponseDTO } from '../lead.models';
import { CompanyResponseDTO } from '../../companies/company.models';
import { ContactResponseDTO } from '../../contacts/contact.models';

describe('LeadList', () => {
  let httpMock: HttpTestingController;
  const leadsBase = `${environment.apiBaseUrl}/leads`;
  const companiesBase = `${environment.apiBaseUrl}/companies`;
  const contactsBase = `${environment.apiBaseUrl}/contacts`;

  const leads: LeadResponseDTO[] = [
    {
      id: 'l1',
      company_id: 'c1',
      contact_id: 'ct1',
      source: 'AI Research',
      status: 'New',
      score: 74,
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

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LeadList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('renders an AI Research badge distinctly from other sources', async () => {
    const fixture = TestBed.createComponent(LeadList);
    fixture.detectChanges();

    httpMock.expectOne(`${leadsBase}?limit=500`).flush(leads);
    httpMock.expectOne(`${companiesBase}?limit=500`).flush(companies);
    httpMock.expectOne(`${contactsBase}?limit=500`).flush(contacts);
    await fixture.whenStable();
    fixture.detectChanges();

    const row = fixture.nativeElement.querySelector('tbody tr');
    expect(row.textContent).toContain('Acme Manufacturing');
    expect(row.textContent).toContain('Jane Doe');
    const sourceBadge = row.querySelector('.badge-ai');
    expect(sourceBadge?.textContent).toContain('AI Research');

    // Status is rendered as a real colored badge too, not plain text and
    // not just an outline -- this lead's status is "New", which maps to
    // the blue info badge (badge-neutral was tried first and found to be
    // visually indistinguishable from plain text on a white table).
    const statusCell = row.querySelectorAll('td')[3];
    const statusBadge = statusCell.querySelector('.badge');
    expect(statusBadge?.classList).toContain('badge-info');
    expect(statusBadge?.textContent).toContain('New');
  });
});
