import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { AssessmentDisplayService } from '../../assessments/assessment-display.service';
import { LeadDisplay, LeadDisplayService } from '../../leads/lead-display.service';
import { QualificationService } from '../qualification.service';
import { QualificationListItemDTO, qualificationStatusBadgeClass } from '../qualification.models';

interface QualificationRow {
  qualification: QualificationListItemDTO;
  leadLabel: string;
  assessmentLabel: string;
}

@Component({
  selector: 'app-qualification-list',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './qualification-list.html',
  styleUrl: './qualification-list.scss',
})
export class QualificationList implements OnInit {
  protected readonly qualificationStatusBadgeClass = qualificationStatusBadgeClass;

  private readonly service = inject(QualificationService);
  private readonly leadDisplayService = inject(LeadDisplayService);
  private readonly assessmentDisplayService = inject(AssessmentDisplayService);

  protected readonly rows = signal<QualificationRow[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    forkJoin({
      qualifications: this.service.list(),
      leads: this.leadDisplayService.loadAll(),
      assessments: this.assessmentDisplayService.loadAll(),
    }).subscribe({
      next: ({ qualifications, leads, assessments }) => {
        this.rows.set(
          qualifications.map((qualification) => ({
            qualification,
            leadLabel: this.leadLabel(qualification.lead_id, leads),
            assessmentLabel:
              assessments.get(qualification.assessment_id)?.discoveryLabel ??
              'Assessment (not found)',
          })),
        );
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load qualifications. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  private leadLabel(leadId: string, leads: Map<string, LeadDisplay>): string {
    const lead = leads.get(leadId);
    return lead ? `${lead.companyName} — ${lead.contactName}` : 'Unknown lead';
  }
}
