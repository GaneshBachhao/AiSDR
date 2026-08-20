import { Component, OnInit, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AssessmentDisplayService } from '../../assessments/assessment-display.service';
import { RecommendationService } from '../recommendation.service';
import {
  RecommendationResponseDTO,
  recommendationStatusBadgeClass,
} from '../recommendation.models';

@Component({
  selector: 'app-recommendation-detail',
  standalone: true,
  imports: [RouterLink, DatePipe],
  templateUrl: './recommendation-detail.html',
  styleUrl: './recommendation-detail.scss',
})
export class RecommendationDetail implements OnInit {
  protected readonly recommendationStatusBadgeClass = recommendationStatusBadgeClass;

  private readonly service = inject(RecommendationService);
  private readonly assessmentDisplayService = inject(AssessmentDisplayService);
  private readonly route = inject(ActivatedRoute);

  protected readonly recommendation = signal<RecommendationResponseDTO | null>(null);
  protected readonly assessmentLabel = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly submitting = signal(false);
  protected readonly approving = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (recommendation) => {
        this.recommendation.set(recommendation);
        this.loading.set(false);
        this.assessmentDisplayService.resolve(recommendation.assessment_id).subscribe({
          next: ({ discoveryLabel }) => this.assessmentLabel.set(discoveryLabel),
        });
      },
      error: () => {
        this.errorMessage.set('Could not load this recommendation. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  submit(): void {
    const recommendation = this.recommendation();
    if (!recommendation) return;
    this.submitting.set(true);
    this.errorMessage.set(null);
    this.service.submit(recommendation.id).subscribe({
      next: (updated) => {
        this.recommendation.set(updated);
        this.submitting.set(false);
      },
      error: () => {
        this.errorMessage.set(
          'Could not submit this recommendation for review. Check that the API is running.',
        );
        this.submitting.set(false);
      },
    });
  }

  approve(): void {
    const recommendation = this.recommendation();
    if (!recommendation) return;
    this.approving.set(true);
    this.errorMessage.set(null);
    this.service.approve(recommendation.id).subscribe({
      next: (updated) => {
        this.recommendation.set(updated);
        this.approving.set(false);
      },
      error: () => {
        this.errorMessage.set(
          'Could not approve this recommendation. Check that the API is running.',
        );
        this.approving.set(false);
      },
    });
  }
}
