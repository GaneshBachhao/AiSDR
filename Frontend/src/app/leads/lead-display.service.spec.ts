import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { LeadDisplayService } from './lead-display.service';
import { LeadResponseDTO } from './lead.models';
import { CompanyResponseDTO } from '../companies/company.models';
import { ContactResponseDTO } from '../contacts/contact.models';

describe('LeadDisplayService', () => {
  let service: LeadDisplayService;
  let httpMock: HttpTestingController;

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

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(LeadDisplayService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('loadAll resolves every lead to its real company and contact names', () => {
    let result: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (result = map));

    httpMock.expectOne(`${environment.apiBaseUrl}/leads?limit=500`).flush([lead]);
    httpMock.expectOne(`${environment.apiBaseUrl}/companies?limit=500`).flush([company]);
    httpMock.expectOne(`${environment.apiBaseUrl}/contacts?limit=500`).flush([contact]);

    expect(result?.get('l1')).toEqual({
      lead,
      companyName: 'Acme Manufacturing',
      contactName: 'Jane Doe',
    });
  });

  it('resolve fetches one lead then its company and contact directly', () => {
    let result: unknown;
    service.resolve('l1').subscribe((r) => (result = r));

    httpMock.expectOne(`${environment.apiBaseUrl}/leads/l1`).flush(lead);
    httpMock.expectOne(`${environment.apiBaseUrl}/companies/c1`).flush(company);
    httpMock.expectOne(`${environment.apiBaseUrl}/contacts/ct1`).flush(contact);

    expect(result).toEqual({
      lead,
      companyName: 'Acme Manufacturing',
      contactName: 'Jane Doe',
    });
  });

  it('a second loadAll() call reuses the cached result instead of re-fetching', () => {
    service.loadAll().subscribe();
    httpMock.expectOne(`${environment.apiBaseUrl}/leads?limit=500`).flush([lead]);
    httpMock.expectOne(`${environment.apiBaseUrl}/companies?limit=500`).flush([company]);
    httpMock.expectOne(`${environment.apiBaseUrl}/contacts?limit=500`).flush([contact]);

    let secondResult: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (secondResult = map));

    // No new HTTP requests -- httpMock.verify() in afterEach would fail
    // if the cache didn't hold, since it asserts no outstanding requests.
    expect(secondResult?.get('l1')).toEqual({
      lead,
      companyName: 'Acme Manufacturing',
      contactName: 'Jane Doe',
    });
  });

  it('invalidate() clears the cache so the next loadAll() re-fetches', () => {
    service.loadAll().subscribe();
    httpMock.expectOne(`${environment.apiBaseUrl}/leads?limit=500`).flush([lead]);
    httpMock.expectOne(`${environment.apiBaseUrl}/companies?limit=500`).flush([company]);
    httpMock.expectOne(`${environment.apiBaseUrl}/contacts?limit=500`).flush([contact]);

    service.invalidate();

    const renamedCompany = { ...company, name: 'Acme Renamed' };
    let secondResult: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (secondResult = map));

    httpMock.expectOne(`${environment.apiBaseUrl}/leads?limit=500`).flush([lead]);
    httpMock.expectOne(`${environment.apiBaseUrl}/companies?limit=500`).flush([renamedCompany]);
    httpMock.expectOne(`${environment.apiBaseUrl}/contacts?limit=500`).flush([contact]);

    expect((secondResult?.get('l1') as { companyName: string }).companyName).toBe('Acme Renamed');
  });
});
