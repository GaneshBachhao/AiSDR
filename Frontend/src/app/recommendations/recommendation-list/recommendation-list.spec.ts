import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { RecommendationList } from './recommendation-list';
import { RecommendationResponseDTO } from '../recommendation.models';
import { AssessmentResponseDTO } from '../../assessments/assessment.models';
import { DiscoveryResponseDTO } from '../../discoveries/discovery.models';

describe('RecommendationList', () => {
  let httpMock: HttpTestingController;
  const base = environment.apiBaseUrl;

  const recommendations: RecommendationResponseDTO[] = [
    {
      id: 'r1',
      assessment_id: 'a1',
      status: 'Draft',
      executive_summary: '3 solution(s) generated from assessment findings.',
      submitted_at: null,
      approved_at: null,
      solutions: [
        {
          solution_id: 's1',
          title: 'Business Process Automation',
          description: 'Automate manual workflows.',
          solution_type: 'Automation',
          priority: 'Critical',
          is_existing_offering: true,
        },
      ],
      roadmap_phases: [],
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    },
  ];
  const assessments: AssessmentResponseDTO[] = [
    {
      assessment_id: 'a1',
      discovery_id: 'd1',
      status: 'Completed',
      summary: null,
      maturity_level: 'Defined',
      readiness_score: 80,
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
      status: 'COMPLETED',
      created_at: '2026-08-16T00:00:00Z',
      updated_at: '2026-08-16T00:00:00Z',
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecommendationList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('renders the resolved assessment label, solution count, and status badge', async () => {
    const fixture = TestBed.createComponent(RecommendationList);
    fixture.detectChanges();

    httpMock.expectOne(`${base}/recommendations?page=1&page_size=200`).flush(recommendations);
    httpMock.expectOne(`${base}/assessments?page=1&page_size=200`).flush(assessments);
    httpMock.expectOne(`${base}/discoveries?limit=500`).flush(discoveries);
    await fixture.whenStable();
    fixture.detectChanges();

    const row = fixture.nativeElement.querySelector('tbody tr');
    expect(row.textContent).toContain('Manual monthly reporting.');
    expect(row.textContent).toContain('1');
    const badge = row.querySelector('.badge');
    expect(badge.classList).toContain('badge-info');
    expect(badge.textContent).toContain('Draft');
  });
});
