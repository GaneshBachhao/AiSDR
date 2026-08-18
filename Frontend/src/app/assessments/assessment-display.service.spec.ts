import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { AssessmentDisplayService } from './assessment-display.service';
import { AssessmentResponseDTO } from './assessment.models';
import { DiscoveryResponseDTO } from '../discoveries/discovery.models';

describe('AssessmentDisplayService', () => {
  let service: AssessmentDisplayService;
  let httpMock: HttpTestingController;
  const base = environment.apiBaseUrl;

  const assessment: AssessmentResponseDTO = {
    assessment_id: 'a1',
    discovery_id: 'd1',
    status: 'Created',
    summary: null,
    maturity_level: 'Initial',
    readiness_score: 0,
    strengths: null,
    weaknesses: null,
    opportunities: null,
    risks: null,
  };
  const discovery: DiscoveryResponseDTO = {
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
    service = TestBed.inject(AssessmentDisplayService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('loadAll resolves every assessment to its discovery problem statement', () => {
    let result: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (result = map));

    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush([assessment]);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush([discovery]);

    expect(result?.get('a1')).toEqual({
      assessment,
      discoveryLabel: 'Manual monthly reporting.',
    });
  });

  it('loadAll falls back to a placeholder when the discovery has no problem statement', () => {
    let result: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (result = map));

    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush([assessment]);
    httpMock
      .expectOne(`${base}/discoveries?limit=500`)
      .flush([{ ...discovery, problem_statement: null }]);

    expect(result?.get('a1')).toEqual({
      assessment,
      discoveryLabel: 'Discovery (no problem statement captured)',
    });
  });

  it('resolve fetches one assessment then its discovery directly', () => {
    let result: unknown;
    service.resolve('a1').subscribe((r) => (result = r));

    httpMock.expectOne(`${base}/assessments/a1`).flush(assessment);
    httpMock.expectOne(`${base}/discoveries/d1`).flush(discovery);

    expect(result).toEqual({
      assessment,
      discoveryLabel: 'Manual monthly reporting.',
    });
  });

  it('a second loadAll() call reuses the cached result instead of re-fetching', () => {
    service.loadAll().subscribe();
    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush([assessment]);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush([discovery]);

    let secondResult: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (secondResult = map));

    expect(secondResult?.get('a1')).toEqual({
      assessment,
      discoveryLabel: 'Manual monthly reporting.',
    });
  });

  it('invalidate() clears the cache so the next loadAll() re-fetches', () => {
    service.loadAll().subscribe();
    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush([assessment]);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush([discovery]);

    service.invalidate();

    const updatedAssessment = { ...assessment, status: 'In Progress' };
    let secondResult: Map<string, unknown> | undefined;
    service.loadAll().subscribe((map) => (secondResult = map));

    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush([updatedAssessment]);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush([discovery]);

    expect(
      (secondResult?.get('a1') as { assessment: AssessmentResponseDTO }).assessment.status,
    ).toBe('In Progress');
  });
});
