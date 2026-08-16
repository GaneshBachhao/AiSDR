import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { DiscoveryService } from '../../discoveries/discovery.service';
import { AssessmentService } from '../assessment.service';
import { AssessmentResponseDTO, assessmentStatusBadgeClass } from '../assessment.models';

@Component({
  selector: 'app-assessment-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './assessment-detail.html',
  styleUrl: './assessment-detail.scss',
})
export class AssessmentDetail implements OnInit {
  protected readonly assessmentStatusBadgeClass = assessmentStatusBadgeClass;

  private readonly service = inject(AssessmentService);
  private readonly discoveryService = inject(DiscoveryService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly assessment = signal<AssessmentResponseDTO | null>(null);
  protected readonly discoveryLabel = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);
  protected readonly starting = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.load();
  }

  private load(): void {
    this.service.get(this.id).subscribe({
      next: (assessment) => {
        this.assessment.set(assessment);
        this.loading.set(false);
        this.discoveryService.get(assessment.discovery_id).subscribe({
          next: (discovery) =>
            this.discoveryLabel.set(discovery.problem_statement ?? 'Discovery (untitled)'),
        });
      },
      error: () => {
        this.errorMessage.set('Could not load this assessment. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  start(): void {
    const assessment = this.assessment();
    if (!assessment) return;
    this.starting.set(true);
    this.errorMessage.set(null);
    this.service.start(assessment.assessment_id).subscribe({
      next: (updated) => {
        this.assessment.set(updated);
        this.starting.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not start this assessment. Check that the API is running.');
        this.starting.set(false);
      },
    });
  }

  delete(): void {
    const assessment = this.assessment();
    if (!assessment) return;
    if (!confirm('Delete this assessment? This cannot be undone.')) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(assessment.assessment_id).subscribe({
      next: () => this.router.navigate(['/assessments']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
