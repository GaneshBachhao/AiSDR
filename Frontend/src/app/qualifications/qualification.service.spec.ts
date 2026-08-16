import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { QualificationService } from './qualification.service';
import { QualificationResponseDTO } from './qualification.models';

describe('QualificationService', () => {
  let service: QualificationService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/qualifications`;

  const sample: QualificationResponseDTO = {
    qualification_id: 'q1',
    lead_id: 'l1',
    assessment_id: 'a1',
    status: 'Partially Qualified',
    score: 0,
    recommendation: null,
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(QualificationService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists qualifications using skip/limit, not page/page_size', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?skip=0&limit=200`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single qualification by id', () => {
    service.get('q1').subscribe();
    const req = httpMock.expectOne(`${base}/q1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('creates a qualification from a lead and assessment id', () => {
    service.create({ lead_id: 'l1', assessment_id: 'a1', status: 'Qualified', score: 88 }).subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ lead_id: 'l1', assessment_id: 'a1', status: 'Qualified', score: 88 });
    req.flush(sample);
  });

  it('updates a qualification', () => {
    service.update('q1', { status: 'Qualified', score: 90 }).subscribe();
    const req = httpMock.expectOne(`${base}/q1`);
    expect(req.request.method).toBe('PUT');
    req.flush(sample);
  });

  it('deletes a qualification', () => {
    service.remove('q1').subscribe();
    const req = httpMock.expectOne(`${base}/q1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
