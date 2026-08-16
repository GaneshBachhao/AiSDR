import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { DashboardCounts, DashboardCountsService } from './dashboard-counts.service';

describe('DashboardCountsService', () => {
  let service: DashboardCountsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(DashboardCountsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('maps each module list endpoint to its array length, using each router\'s real pagination params', () => {
    let result: DashboardCounts | undefined;
    service.load().subscribe((counts) => (result = counts));

    const respond = (url: string, count: number) => {
      const req = httpMock.expectOne(url);
      req.flush(Array.from({ length: count }, (_, i) => ({ id: i })));
    };

    // skip/limit modules
    respond(`${environment.apiBaseUrl}/companies?limit=500`, 8);
    respond(`${environment.apiBaseUrl}/contacts?limit=500`, 3);
    respond(`${environment.apiBaseUrl}/leads?limit=500`, 3);
    respond(`${environment.apiBaseUrl}/discoveries?limit=500`, 3);
    respond(`${environment.apiBaseUrl}/qualifications?limit=200`, 0);

    // page/page_size modules -- NOT `limit` (the bug this test guards against)
    respond(`${environment.apiBaseUrl}/assessments?page=1&page_size=200`, 2);
    respond(`${environment.apiBaseUrl}/recommendations?page=1&page_size=200`, 1);

    expect(result).toEqual({
      companies: 8,
      contacts: 3,
      leads: 3,
      discoveries: 3,
      assessments: 2,
      qualifications: 0,
      recommendations: 1,
    });
  });
});
