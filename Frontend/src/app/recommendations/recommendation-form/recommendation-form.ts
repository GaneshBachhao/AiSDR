import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import {
  AssessmentDisplay,
  AssessmentDisplayService,
} from '../../assessments/assessment-display.service';
import { RecommendationService } from '../recommendation.service';

/** Not a plain "create" form -- there's no free-text fields to fill in,
 * just an Assessment to generate against (GenerateRecommendationRequest
 * has exactly one field). The backend runs a real AI call to produce the
 * Solutions, and is idempotent per assessment_id (re-generating for an
 * Assessment that already has one just returns it, not a duplicate). */
@Component({
  selector: 'app-recommendation-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './recommendation-form.html',
  styleUrl: './recommendation-form.scss',
})
export class RecommendationForm implements OnInit {
  private readonly service = inject(RecommendationService);
  private readonly assessmentDisplayService = inject(AssessmentDisplayService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly assessmentId = signal('');
  protected readonly assessmentOptions = signal<[string, AssessmentDisplay][]>([]);

  protected readonly generating = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.assessmentId.set(this.route.snapshot.queryParamMap.get('assessment_id') ?? '');
    this.assessmentDisplayService.loadAll().subscribe({
      next: (assessments) => this.assessmentOptions.set([...assessments.entries()]),
      error: () => this.errorMessage.set('Could not load assessments for the picker.'),
    });
  }

  generate(): void {
    this.generating.set(true);
    this.errorMessage.set(null);
    this.service.generate({ assessment_id: this.assessmentId() }).subscribe({
      next: (recommendation) => this.router.navigate(['/recommendations', recommendation.id]),
      error: (err) => {
        this.errorMessage.set(this.describeError(err));
        this.generating.set(false);
      },
    });
  }

  private describeError(err: unknown): string {
    if (err && typeof err === 'object' && 'error' in err) {
      const body = (err as { error?: { message?: string; detail?: string } }).error;
      if (body?.message) return body.message;
      if (body?.detail) return body.detail;
    }
    return 'Generation failed. Check that the API is running and the AI provider is configured.';
  }
}
