import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { DiscoveryService } from '../../discoveries/discovery.service';
import { DiscoveryResponseDTO } from '../../discoveries/discovery.models';
import { AssessmentService } from '../assessment.service';
import { AssessmentResponseDTO, assessmentStatusBadgeClass } from '../assessment.models';

@Component({
  selector: 'app-assessment-list',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './assessment-list.html',
  styleUrl: './assessment-list.scss',
})
export class AssessmentList implements OnInit {
  protected readonly assessmentStatusBadgeClass = assessmentStatusBadgeClass;

  private readonly assessmentService = inject(AssessmentService);
  private readonly discoveryService = inject(DiscoveryService);

  protected readonly assessments = signal<AssessmentResponseDTO[]>([]);
  private readonly discoveryById = signal<Map<string, DiscoveryResponseDTO>>(new Map());
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);

  protected discoveryLabelFor(assessment: AssessmentResponseDTO): string {
    const discovery = this.discoveryById().get(assessment.discovery_id);
    return discovery?.problem_statement ?? 'Discovery (no problem statement captured)';
  }

  ngOnInit(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    forkJoin({
      assessments: this.assessmentService.list(),
      discoveries: this.discoveryService.list(),
    }).subscribe({
      next: ({ assessments, discoveries }) => {
        this.assessments.set(assessments);
        this.discoveryById.set(new Map(discoveries.map((d) => [d.id, d])));
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load assessments. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }
}
