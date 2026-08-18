import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { DashboardCounts, DashboardCountsService } from './dashboard-counts.service';

interface Kpi {
  label: string;
  path: string;
  value: () => number | null;
}

interface PipelineStage {
  label: string;
  path: string;
  value: () => number | null;
}

@Component({
  selector: 'app-command-center',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './command-center.html',
  styleUrl: './command-center.scss',
})
export class CommandCenter implements OnInit {
  private readonly service = inject(DashboardCountsService);

  protected readonly counts = signal<DashboardCounts | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);

  protected readonly kpis: Kpi[] = [
    { label: 'Companies', path: '/companies', value: () => this.counts()?.companies ?? null },
    { label: 'Contacts', path: '/contacts', value: () => this.counts()?.contacts ?? null },
    { label: 'Leads', path: '/leads', value: () => this.counts()?.leads ?? null },
    {
      label: 'Recommendations',
      path: '/recommendations',
      value: () => this.counts()?.recommendations ?? null,
    },
  ];

  /** Real pipeline order (Company → Lead → Discovery → Assessment →
   * Qualification) -- see Frontend/docs/design_system.md §2. There's no
   * persisted "Researched" stage to show, since company_research doesn't
   * persist by default, so this starts from Companies, not a research count. */
  protected readonly pipeline: PipelineStage[] = [
    { label: 'Companies', path: '/companies', value: () => this.counts()?.companies ?? null },
    { label: 'Leads', path: '/leads', value: () => this.counts()?.leads ?? null },
    {
      label: 'Discoveries',
      path: '/discoveries',
      value: () => this.counts()?.discoveries ?? null,
    },
    {
      label: 'Assessments',
      path: '/assessments',
      value: () => this.counts()?.assessments ?? null,
    },
    {
      label: 'Qualifications',
      path: '/qualifications',
      value: () => this.counts()?.qualifications ?? null,
    },
  ];

  ngOnInit(): void {
    this.service.load().subscribe({
      next: (counts) => {
        this.counts.set(counts);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load dashboard counts. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }
}
