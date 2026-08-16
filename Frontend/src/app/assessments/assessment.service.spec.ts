import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { AssessmentService } from './assessment.service';
import { AssessmentResponseDTO } from './assessment.models';

describe('AssessmentService', () => {
  let service: AssessmentService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/assessments`;

  const sample: AssessmentResponseDTO = {
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

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(AssessmentService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists assessments using page/page_size, not limit', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?page=1&page_size=200`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single assessment by id', () => {
    service.get('a1').subscribe();
    const req = httpMock.expectOne(`${base}/a1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('creates an assessment from a discovery id only', () => {
    service.create({ discovery_id: 'd1' }).subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ discovery_id: 'd1' });
    req.flush(sample);
  });

  it('updates an assessment', () => {
    service.update('a1', { summary: 'Solid fit' }).subscribe();
    const req = httpMock.expectOne(`${base}/a1`);
    expect(req.request.method).toBe('PUT');
    req.flush(sample);
  });

  it('starts an assessment with an empty body', () => {
    service.start('a1').subscribe();
    const req = httpMock.expectOne(`${base}/a1/start`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({});
    req.flush({ ...sample, status: 'In Progress' });
  });

  it('deletes an assessment', () => {
    service.remove('a1').subscribe();
    const req = httpMock.expectOne(`${base}/a1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
