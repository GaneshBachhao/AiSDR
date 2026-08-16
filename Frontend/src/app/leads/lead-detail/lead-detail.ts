import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { LeadDisplayService } from '../lead-display.service';
import { LeadService } from '../lead.service';
import { LeadResponseDTO, leadStatusBadgeClass } from '../lead.models';

@Component({
  selector: 'app-lead-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './lead-detail.html',
  styleUrl: './lead-detail.scss',
})
export class LeadDetail implements OnInit {
  protected readonly leadStatusBadgeClass = leadStatusBadgeClass;

  private readonly service = inject(LeadService);
  private readonly displayService = inject(LeadDisplayService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly lead = signal<LeadResponseDTO | null>(null);
  protected readonly companyName = signal<string | null>(null);
  protected readonly contactName = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.displayService.resolve(this.id).subscribe({
      next: ({ lead, companyName, contactName }) => {
        this.lead.set(lead);
        this.companyName.set(companyName);
        this.contactName.set(contactName);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load this lead. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  delete(): void {
    const lead = this.lead();
    if (!lead) return;
    if (!confirm('Delete this lead? This cannot be undone.')) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(lead.id).subscribe({
      next: () => this.router.navigate(['/leads']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
