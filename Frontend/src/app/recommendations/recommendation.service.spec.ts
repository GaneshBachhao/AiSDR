import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { RecommendationService } from './recommendation.service';
import { RecommendationResponseDTO } from './recommendation.models';

describe('RecommendationService', () => {
  let service: RecommendationService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/recommendations`;

  const sample: RecommendationResponseDTO = {
    id: 'r1',
    assessment_id: 'a1',
    status: 'Draft',
    executive_summary: '3 solution(s) generated from assessment findings.',
    submitted_at: null,
    approved_at: null,
    solutions: [],
    roadmap_phases: [],
    created_at: '2026-08-16T00:00:00Z',
    updated_at: '2026-08-16T00:00:00Z',
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(RecommendationService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists recommendations using page/page_size', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?page=1&page_size=200`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single recommendation by id', () => {
    service.get('r1').subscribe();
    const req = httpMock.expectOne(`${base}/r1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('generates a recommendation from an assessment id', () => {
    service.generate({ assessment_id: 'a1' }).subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ assessment_id: 'a1' });
    req.flush(sample);
  });
});
