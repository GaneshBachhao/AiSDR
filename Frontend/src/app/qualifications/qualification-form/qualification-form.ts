import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import {
  AssessmentDisplay,
  AssessmentDisplayService,
} from '../../assessments/assessment-display.service';
import { LeadDisplay, LeadDisplayService } from '../../leads/lead-display.service';
import { QualificationService } from '../qualification.service';
import {
  CreateQualificationRequestDTO,
  QUALIFICATION_STATUSES,
  UpdateQualificationRequestDTO,
  emptyQualificationForm,
} from '../qualification.models';

@Component({
  selector: 'app-qualification-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './qualification-form.html',
  styleUrl: './qualification-form.scss',
})
export class QualificationForm implements OnInit {
  private readonly service = inject(QualificationService);
  private readonly leadDisplayService = inject(LeadDisplayService);
  private readonly assessmentDisplayService = inject(AssessmentDisplayService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly statuses = QUALIFICATION_STATUSES;

  protected readonly qualificationId = signal<string | null>(null);
  protected readonly isEditMode = signal(false);

  // Create mode only -- lead_id/assessment_id aren't on
  // UpdateQualificationRequestDTO, so they're create-time-only, same as
  // every other module's parent link.
  protected readonly form = signal<CreateQualificationRequestDTO>(emptyQualificationForm());
  protected readonly leadOptions = signal<[string, LeadDisplay][]>([]);
  protected readonly assessmentOptions = signal<[string, AssessmentDisplay][]>([]);

  // Edit mode only.
  protected readonly leadLabel = signal<string | null>(null);
  protected readonly assessmentLabel = signal<string | null>(null);

  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.qualificationId.set(id);
      this.isEditMode.set(true);
      this.loading.set(true);
      this.service.get(id).subscribe({
        next: (qualification) => {
          this.form.set({
            lead_id: qualification.lead_id,
            assessment_id: qualification.assessment_id,
            status: qualification.status,
            score: qualification.score,
            recommendation: qualification.recommendation,
          });
          this.leadDisplayService.resolve(qualification.lead_id).subscribe({
            next: ({ companyName, contactName }) =>
              this.leadLabel.set(`${companyName} — ${contactName}`),
          });
          this.assessmentDisplayService.resolve(qualification.assessment_id).subscribe({
            next: ({ discoveryLabel }) => this.assessmentLabel.set(discoveryLabel),
          });
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set(
            'Could not load this qualification. Check that the API is running.',
          );
          this.loading.set(false);
        },
      });
      return;
    }

    const params = this.route.snapshot.queryParamMap;
    this.form.set(
      emptyQualificationForm(params.get('lead_id') ?? '', params.get('assessment_id') ?? ''),
    );

    this.leadDisplayService.loadAll().subscribe({
      next: (leads) => this.leadOptions.set([...leads.entries()]),
      error: () => this.errorMessage.set('Could not load leads for the picker.'),
    });
    this.assessmentDisplayService.loadAll().subscribe({
      next: (assessments) => this.assessmentOptions.set([...assessments.entries()]),
      error: () => this.errorMessage.set('Could not load assessments for the picker.'),
    });
  }

  updateForm<K extends keyof CreateQualificationRequestDTO>(
    field: K,
    value: CreateQualificationRequestDTO[K],
  ): void {
    this.form.update((f) => ({ ...f, [field]: value }));
  }

  save(): void {
    this.saving.set(true);
    this.errorMessage.set(null);
    const id = this.qualificationId();

    const request = id
      ? this.service.update(id, this.toUpdateDto())
      : this.service.create(this.form());

    request.subscribe({
      next: (qualification) =>
        this.router.navigate(['/qualifications', qualification.qualification_id]),
      error: (err) => {
        this.errorMessage.set(this.describeError(err));
        this.saving.set(false);
      },
    });
  }

  private toUpdateDto(): UpdateQualificationRequestDTO {
    const { status, score, recommendation } = this.form();
    return { status, score, recommendation };
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
