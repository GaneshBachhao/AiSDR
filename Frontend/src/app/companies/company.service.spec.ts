import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { CompanyService } from './company.service';
import { CompanyResponseDTO } from './company.models';

describe('CompanyService', () => {
  let service: CompanyService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/companies`;

  const sample: CompanyResponseDTO = {
    id: 'c1',
    name: 'Acme Manufacturing',
    website: 'https://acme.example',
    industry: 'Manufacturing',
    company_size: 'Large',
    employee_count: 250,
    country: 'India',
    state: null,
    city: null,
    is_active: true,
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(CompanyService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists companies with a generous limit', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('searches companies by query', () => {
    service.search('acme').subscribe();
    const req = httpMock.expectOne(`${base}/search?query=acme&limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single company by id', () => {
    service.get('c1').subscribe();
    const req = httpMock.expectOne(`${base}/c1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('creates a company', () => {
    service.create({ name: 'Acme Manufacturing' }).subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ name: 'Acme Manufacturing' });
    req.flush(sample);
  });

  it('updates a company', () => {
    service.update('c1', { name: 'Acme Mfg' }).subscribe();
    const req = httpMock.expectOne(`${base}/c1`);
    expect(req.request.method).toBe('PUT');
    req.flush(sample);
  });

  it('deletes a company', () => {
    service.remove('c1').subscribe();
    const req = httpMock.expectOne(`${base}/c1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
