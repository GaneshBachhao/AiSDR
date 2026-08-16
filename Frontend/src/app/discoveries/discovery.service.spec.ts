import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { DiscoveryService } from './discovery.service';
import { DiscoveryResponseDTO } from './discovery.models';

describe('DiscoveryService', () => {
  let service: DiscoveryService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/discoveries`;

  const sample: DiscoveryResponseDTO = {
    id: 'd1',
    lead_id: 'l1',
    problem_statement: 'Manual monthly reporting.',
    current_solution: null,
    business_impact: null,
    success_criteria: null,
    status: 'CREATED',
    created_at: '2026-08-16T00:00:00Z',
    updated_at: '2026-08-16T00:00:00Z',
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(DiscoveryService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists discoveries with a generous limit', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('searches discoveries using search_text', () => {
    service.search('reporting').subscribe();
    const req = httpMock.expectOne(`${base}/search?search_text=reporting&limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single discovery by id', () => {
    service.get('d1').subscribe();
    const req = httpMock.expectOne(`${base}/d1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('creates a discovery', () => {
    service.create({ lead_id: 'l1', problem_statement: 'x' }).subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    req.flush(sample);
  });

  it('updates a discovery', () => {
    service.update('d1', { status: 'IN_PROGRESS' }).subscribe();
    const req = httpMock.expectOne(`${base}/d1`);
    expect(req.request.method).toBe('PUT');
    req.flush(sample);
  });

  it('deletes a discovery', () => {
    service.remove('d1').subscribe();
    const req = httpMock.expectOne(`${base}/d1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
