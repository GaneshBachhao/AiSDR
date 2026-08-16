import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { AssessmentDisplayService } from '../../assessments/assessment-display.service';
import { LeadDisplayService } from '../../leads/lead-display.service';
import { QualificationService } from '../qualification.service';
import { QualificationResponseDTO, qualificationStatusBadgeClass } from '../qualification.models';

@Component({
  selector: 'app-qualification-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './qualification-detail.html',
  styleUrl: './qualification-detail.scss',
})
export class QualificationDetail implements OnInit {
  protected readonly qualificationStatusBadgeClass = qualificationStatusBadgeClass;

  private readonly service = inject(QualificationService);
  private readonly leadDisplayService = inject(LeadDisplayService);
  private readonly assessmentDisplayService = inject(AssessmentDisplayService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly qualification = signal<QualificationResponseDTO | null>(null);
  protected readonly leadLabel = signal<string | null>(null);
  protected readonly assessmentLabel = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (qualification) => {
        this.qualification.set(qualification);
        this.loading.set(false);
        forkJoin({
          lead: this.leadDisplayService.resolve(qualification.lead_id),
          assessment: this.assessmentDisplayService.resolve(qualification.assessment_id),
        }).subscribe({
          next: ({ lead, assessment }) => {
            this.leadLabel.set(`${lead.companyName} — ${lead.contactName}`);
            this.assessmentLabel.set(assessment.discoveryLabel);
          },
        });
      },
      error: () => {
        this.errorMessage.set('Could not load this qualification. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  delete(): void {
    const qualification = this.qualification();
    if (!qualification) return;
    if (!confirm('Delete this qualification? This cannot be undone.')) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(qualification.qualification_id).subscribe({
      next: () => this.router.navigate(['/qualifications']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
