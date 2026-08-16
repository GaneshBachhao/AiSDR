import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AssessmentDisplay, AssessmentDisplayService } from '../assessment-display.service';
import { assessmentStatusBadgeClass } from '../assessment.models';

@Component({
  selector: 'app-assessment-list',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './assessment-list.html',
  styleUrl: './assessment-list.scss',
})
export class AssessmentList implements OnInit {
  protected readonly assessmentStatusBadgeClass = assessmentStatusBadgeClass;

  private readonly displayService = inject(AssessmentDisplayService);

  protected readonly assessments = signal<AssessmentDisplay[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.displayService.loadAll().subscribe({
      next: (displays) => {
        this.assessments.set([...displays.values()]);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load assessments. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }
}
