import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { AssessmentDisplayService } from '../../assessments/assessment-display.service';
import { RecommendationService } from '../recommendation.service';
import {
  RecommendationResponseDTO,
  recommendationStatusBadgeClass,
} from '../recommendation.models';

interface RecommendationRow {
  recommendation: RecommendationResponseDTO;
  assessmentLabel: string;
}

@Component({
  selector: 'app-recommendation-list',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './recommendation-list.html',
  styleUrl: './recommendation-list.scss',
})
export class RecommendationList implements OnInit {
  protected readonly recommendationStatusBadgeClass = recommendationStatusBadgeClass;

  private readonly service = inject(RecommendationService);
  private readonly assessmentDisplayService = inject(AssessmentDisplayService);

  protected readonly rows = signal<RecommendationRow[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    forkJoin({
      recommendations: this.service.list(),
      assessments: this.assessmentDisplayService.loadAll(),
    }).subscribe({
      next: ({ recommendations, assessments }) => {
        this.rows.set(
          recommendations.map((recommendation) => ({
            recommendation,
            assessmentLabel:
              assessments.get(recommendation.assessment_id)?.discoveryLabel ??
              'Assessment (not found)',
          })),
        );
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load recommendations. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }
}
