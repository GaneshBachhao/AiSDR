import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { LeadDisplay, LeadDisplayService } from '../../leads/lead-display.service';
import { DiscoveryService } from '../discovery.service';
import {
  CreateDiscoveryRequestDTO,
  DISCOVERY_STATUSES,
  DiscoveryStatus,
  emptyDiscoveryForm,
} from '../discovery.models';

@Component({
  selector: 'app-discovery-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './discovery-form.html',
  styleUrl: './discovery-form.scss',
})
export class DiscoveryForm implements OnInit {
  private readonly service = inject(DiscoveryService);
  private readonly leadDisplayService = inject(LeadDisplayService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly statuses = DISCOVERY_STATUSES;

  protected readonly discoveryId = signal<string | null>(null);
  protected readonly isEditMode = signal(false);
  protected readonly form = signal<CreateDiscoveryRequestDTO>(emptyDiscoveryForm());
  protected readonly status = signal<DiscoveryStatus>('CREATED');
  protected readonly leadLabel = signal<string | null>(null);
  protected readonly leadOptions = signal<LeadDisplay[]>([]);

  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.discoveryId.set(id);
      this.isEditMode.set(true);
      this.loading.set(true);
      this.service.get(id).subscribe({
        next: (discovery) => {
          this.form.set({
            lead_id: discovery.lead_id,
            problem_statement: discovery.problem_statement,
            current_solution: discovery.current_solution,
            business_impact: discovery.business_impact,
            success_criteria: discovery.success_criteria,
          });
          this.status.set(discovery.status as DiscoveryStatus);
          this.leadDisplayService.resolve(discovery.lead_id).subscribe({
            next: ({ companyName, contactName }) =>
              this.leadLabel.set(`${companyName} — ${contactName}`),
          });
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('Could not load this discovery. Check that the API is running.');
          this.loading.set(false);
        },
      });
      return;
    }

    const preselectedLeadId = this.route.snapshot.queryParamMap.get('lead_id') ?? '';
    this.form.set(emptyDiscoveryForm(preselectedLeadId));
    this.leadDisplayService.loadAll().subscribe({
      next: (byId) => this.leadOptions.set(Array.from(byId.values())),
      error: () => this.errorMessage.set('Could not load leads for the picker.'),
    });
  }

  update(field: keyof CreateDiscoveryRequestDTO, value: string): void {
    this.form.update((f) => ({ ...f, [field]: value.trim() === '' ? null : value }));
  }

  save(): void {
    this.saving.set(true);
    this.errorMessage.set(null);
    const id = this.discoveryId();

    const request = id
      ? this.service.update(id, {
          problem_statement: this.form().problem_statement,
          current_solution: this.form().current_solution,
          business_impact: this.form().business_impact,
          success_criteria: this.form().success_criteria,
          status: this.status(),
        })
      : this.service.create(this.form());

    request.subscribe({
      next: (discovery) => this.router.navigate(['/discoveries', discovery.id]),
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
