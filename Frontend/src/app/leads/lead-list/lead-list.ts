import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { LeadDisplay, LeadDisplayService } from '../lead-display.service';
import { LeadService } from '../lead.service';
import { LeadResponseDTO, leadStatusBadgeClass } from '../lead.models';

@Component({
  selector: 'app-lead-list',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './lead-list.html',
  styleUrl: './lead-list.scss',
})
export class LeadList implements OnInit {
  protected readonly leadStatusBadgeClass = leadStatusBadgeClass;

  private readonly leadService = inject(LeadService);
  private readonly displayService = inject(LeadDisplayService);

  protected readonly leads = signal<LeadResponseDTO[]>([]);
  /** Built once from the full universe of leads/companies/contacts;
   * reused across searches since a search result is always a subset of
   * that same universe -- no need to refetch companies/contacts per
   * search. */
  private readonly displayById = signal<Map<string, LeadDisplay>>(new Map());
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly searchQuery = signal('');

  protected companyNameFor(lead: LeadResponseDTO): string {
    return this.displayById().get(lead.id)?.companyName ?? '—';
  }

  protected contactNameFor(lead: LeadResponseDTO): string {
    return this.displayById().get(lead.id)?.contactName ?? '—';
  }

  ngOnInit(): void {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.displayService.loadAll().subscribe({
      next: (displayById) => {
        this.displayById.set(displayById);
        this.leads.set(Array.from(displayById.values()).map((d) => d.lead));
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load leads. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  search(): void {
    const keyword = this.searchQuery().trim();
    if (!keyword) {
      this.load();
      return;
    }
    this.loading.set(true);
    this.errorMessage.set(null);
    this.leadService.search(keyword).subscribe({
      next: (leads) => {
        this.leads.set(leads);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Search failed. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  clearSearch(): void {
    this.searchQuery.set('');
    this.load();
  }
}
