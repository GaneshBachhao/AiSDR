import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { LeadService } from './lead.service';
import { LeadResponseDTO } from './lead.models';

describe('LeadService', () => {
  let service: LeadService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/leads`;

  const sample: LeadResponseDTO = {
    id: 'l1',
    company_id: 'c1',
    contact_id: 'ct1',
    source: 'Other',
    status: 'New',
    score: 0,
    notes: null,
    is_qualified: false,
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(LeadService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists leads with a generous limit', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('searches leads using keyword, not query or search_text', () => {
    service.search('acme').subscribe();
    const req = httpMock.expectOne(`${base}/search?keyword=acme&limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single lead by id', () => {
    service.get('l1').subscribe();
    const req = httpMock.expectOne(`${base}/l1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('creates a lead', () => {
    service
      .create({
        company_id: 'c1',
        contact_id: 'ct1',
        source: 'AI Research',
        score: 74,
        notes: null,
      })
      .subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    expect(req.request.body.source).toBe('AI Research');
    req.flush(sample);
  });

  it('updates a lead', () => {
    service.update('l1', { status: 'Qualified' }).subscribe();
    const req = httpMock.expectOne(`${base}/l1`);
    expect(req.request.method).toBe('PUT');
    req.flush(sample);
  });

  it('deletes a lead', () => {
    service.remove('l1').subscribe();
    const req = httpMock.expectOne(`${base}/l1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
