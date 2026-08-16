import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { DiscoveryService } from '../../discoveries/discovery.service';
import { DiscoveryResponseDTO } from '../../discoveries/discovery.models';
import { AssessmentService } from '../assessment.service';
import { MATURITY_LEVELS, UpdateAssessmentRequestDTO } from '../assessment.models';

@Component({
  selector: 'app-assessment-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './assessment-form.html',
  styleUrl: './assessment-form.scss',
})
export class AssessmentForm implements OnInit {
  private readonly service = inject(AssessmentService);
  private readonly discoveryService = inject(DiscoveryService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly maturityLevels = MATURITY_LEVELS;

  protected readonly assessmentId = signal<string | null>(null);
  protected readonly isEditMode = signal(false);

  // Create mode only -- CreateAssessmentRequestDTO has just discovery_id.
  protected readonly discoveryId = signal('');
  protected readonly discoveryOptions = signal<DiscoveryResponseDTO[]>([]);
  protected readonly discoveryLabel = signal<string | null>(null);

  // Edit mode only -- everything UpdateAssessmentRequestDTO supports.
  // Status is deliberately not editable here: the only status transition
  // the API exposes is the dedicated /start action (Created -> In
  // Progress); Under Review/Completed/Cancelled have no reachable
  // endpoint today, so this form doesn't pretend otherwise.
  protected readonly form = signal<UpdateAssessmentRequestDTO>({});

  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.assessmentId.set(id);
      this.isEditMode.set(true);
      this.loading.set(true);
      this.service.get(id).subscribe({
        next: (assessment) => {
          this.form.set({
            summary: assessment.summary,
            maturity_level: assessment.maturity_level,
            readiness_score: assessment.readiness_score,
            strengths: assessment.strengths,
            weaknesses: assessment.weaknesses,
            opportunities: assessment.opportunities,
            risks: assessment.risks,
          });
          this.discoveryService.get(assessment.discovery_id).subscribe({
            next: (discovery) =>
              this.discoveryLabel.set(discovery.problem_statement ?? 'Discovery (untitled)'),
          });
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('Could not load this assessment. Check that the API is running.');
          this.loading.set(false);
        },
      });
      return;
    }

    this.discoveryId.set(this.route.snapshot.queryParamMap.get('discovery_id') ?? '');
    this.discoveryService.list().subscribe({
      next: (discoveries) => this.discoveryOptions.set(discoveries),
      error: () => this.errorMessage.set('Could not load discoveries for the picker.'),
    });
  }

  update<K extends keyof UpdateAssessmentRequestDTO>(field: K, value: UpdateAssessmentRequestDTO[K]): void {
    this.form.update((f) => ({ ...f, [field]: value }));
  }

  save(): void {
    this.saving.set(true);
    this.errorMessage.set(null);
    const id = this.assessmentId();

    const request = id
      ? this.service.update(id, this.form())
      : this.service.create({ discovery_id: this.discoveryId() });

    request.subscribe({
      next: (assessment) => this.router.navigate(['/assessments', assessment.assessment_id]),
      error: (err) => {
        this.errorMessage.set(this.describeError(err));
        this.saving.set(false);
      },
    });
  }

  private describeError(err: unknown): string {
    if (err && typeof err === 'object' && 'error' in err) {
      const body = (err as { error?: { message?: string; detail?: string } }).error;
      if (body?.message) return body.message;
      if (body?.detail) return body.detail;
    }
    return 'Save failed. Check that the API is running.';
  }
}
