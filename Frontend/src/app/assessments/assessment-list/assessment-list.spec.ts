import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { AssessmentList } from './assessment-list';
import { AssessmentResponseDTO } from '../assessment.models';
import { DiscoveryResponseDTO } from '../../discoveries/discovery.models';

describe('AssessmentList', () => {
  let httpMock: HttpTestingController;
  const base = environment.apiBaseUrl;

  const assessments: AssessmentResponseDTO[] = [
    {
      assessment_id: 'a1',
      discovery_id: 'd1',
      status: 'In Progress',
      summary: null,
      maturity_level: 'Developing',
      readiness_score: 62,
      strengths: null,
      weaknesses: null,
      opportunities: null,
      risks: null,
    },
  ];
  const discoveries: DiscoveryResponseDTO[] = [
    {
      id: 'd1',
      lead_id: 'l1',
      problem_statement: 'Manual monthly reporting.',
      current_solution: null,
      business_impact: null,
      success_criteria: null,
      status: 'IN_PROGRESS',
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssessmentList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('renders the resolved discovery label, maturity, readiness, and status badge', async () => {
    const fixture = TestBed.createComponent(AssessmentList);
    fixture.detectChanges();

    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush(assessments);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush(discoveries);
    await fixture.whenStable();
    fixture.detectChanges();

    const row = fixture.nativeElement.querySelector('tbody tr');
    expect(row.textContent).toContain('Manual monthly reporting.');
    expect(row.textContent).toContain('Developing');
    expect(row.textContent).toContain('62');
    const badge = row.querySelector('.badge');
    expect(badge.classList).toContain('badge-warn');
    expect(badge.textContent).toContain('In Progress');
  });
});
