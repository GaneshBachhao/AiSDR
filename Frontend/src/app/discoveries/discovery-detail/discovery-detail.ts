import { Component, OnInit, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AssessmentService } from '../../assessments/assessment.service';
import {
  AssessmentResponseDTO,
  assessmentStatusBadgeClass,
} from '../../assessments/assessment.models';
import { LeadDisplayService } from '../../leads/lead-display.service';
import { RecommendationService } from '../../recommendations/recommendation.service';
import {
  RecommendationResponseDTO,
  recommendationStatusBadgeClass,
} from '../../recommendations/recommendation.models';
import { DiscoveryService } from '../discovery.service';
import {
  DiscoveryResponseDTO,
  discoveryCompleteness,
  discoveryStatusBadgeClass,
} from '../discovery.models';

@Component({
  selector: 'app-discovery-detail',
  standalone: true,
  imports: [RouterLink, DatePipe],
  templateUrl: './discovery-detail.html',
  styleUrl: './discovery-detail.scss',
})
export class DiscoveryDetail implements OnInit {
  protected readonly discoveryStatusBadgeClass = discoveryStatusBadgeClass;
  protected readonly discoveryCompleteness = discoveryCompleteness;
  protected readonly assessmentStatusBadgeClass = assessmentStatusBadgeClass;
  protected readonly recommendationStatusBadgeClass = recommendationStatusBadgeClass;

  private readonly service = inject(DiscoveryService);
  private readonly leadDisplayService = inject(LeadDisplayService);
  private readonly assessmentService = inject(AssessmentService);
  private readonly recommendationService = inject(RecommendationService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly discovery = signal<DiscoveryResponseDTO | null>(null);
  protected readonly leadId = signal<string | null>(null);
  protected readonly leadLabel = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  // Cross-entity drill-down (EPIC-F10): a Discovery has at most one
  // Assessment (see AssessmentService.listByDiscovery's own comment on
  // the unique-constraint backing that), so once one exists the "+ Add
  // Assessment" create link is replaced with a link to the real one --
  // clicking create again would hit that unique constraint and 500.
  protected readonly assessment = signal<AssessmentResponseDTO | null>(null);
  protected readonly recommendation = signal<RecommendationResponseDTO | null>(null);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (discovery) => {
        this.discovery.set(discovery);
        this.leadId.set(discovery.lead_id);
        this.loading.set(false);
        this.leadDisplayService.resolve(discovery.lead_id).subscribe({
          next: ({ companyName, contactName }) =>
            this.leadLabel.set(`${companyName} — ${contactName}`),
        });
        this.loadAssessment(discovery.id);
      },
      error: () => {
        this.errorMessage.set('Could not load this discovery. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  private loadAssessment(discoveryId: string): void {
    this.assessmentService.listByDiscovery(discoveryId).subscribe({
      next: (assessments) => {
        const assessment = assessments[0] ?? null;
        this.assessment.set(assessment);
        if (assessment) {
          this.loadRecommendation(assessment.assessment_id);
        }
      },
    });
  }

  // No assessment_id filter exists on GET /recommendations (verified
  // against the schema), so this fetches the (small, capped) full list
  // and filters client-side, same as AssessmentDisplayService does for
  // Discovery labels.
  private loadRecommendation(assessmentId: string): void {
    this.recommendationService.list().subscribe({
      next: (recommendations) => {
        this.recommendation.set(
          recommendations.find((r) => r.assessment_id === assessmentId) ?? null,
        );
      },
    });
  }

  delete(): void {
    const discovery = this.discovery();
    if (!discovery) return;
    if (!confirm('Delete this discovery? This cannot be undone.')) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(discovery.id).subscribe({
      next: () => this.router.navigate(['/discoveries']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
