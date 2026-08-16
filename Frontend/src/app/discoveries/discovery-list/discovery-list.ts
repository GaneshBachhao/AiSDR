import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { LeadDisplay, LeadDisplayService } from '../../leads/lead-display.service';
import { DiscoveryService } from '../discovery.service';
import {
  DiscoveryResponseDTO,
  discoveryCompleteness,
  discoveryStatusBadgeClass,
} from '../discovery.models';

@Component({
  selector: 'app-discovery-list',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './discovery-list.html',
  styleUrl: './discovery-list.scss',
})
export class DiscoveryList implements OnInit {
  protected readonly discoveryStatusBadgeClass = discoveryStatusBadgeClass;
  protected readonly discoveryCompleteness = discoveryCompleteness;

  private readonly discoveryService = inject(DiscoveryService);
  private readonly leadDisplayService = inject(LeadDisplayService);

  protected readonly discoveries = signal<DiscoveryResponseDTO[]>([]);
  private readonly leadDisplayById = signal<Map<string, LeadDisplay>>(new Map());
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly searchQuery = signal('');

  protected leadLabelFor(discovery: DiscoveryResponseDTO): string {
    const display = this.leadDisplayById().get(discovery.lead_id);
    return display ? `${display.companyName} — ${display.contactName}` : '—';
  }

  ngOnInit(): void {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.leadDisplayService.loadAll().subscribe({
      next: (leadDisplayById) => {
        this.leadDisplayById.set(leadDisplayById);
        this.discoveryService.list().subscribe({
          next: (discoveries) => {
            this.discoveries.set(discoveries);
            this.loading.set(false);
          },
          error: () => {
            this.errorMessage.set('Could not load discoveries. Check that the API is running.');
            this.loading.set(false);
          },
        });
      },
      error: () => {
        this.errorMessage.set('Could not load leads for display. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  search(): void {
    const text = this.searchQuery().trim();
    if (!text) {
      this.load();
      return;
    }
    this.loading.set(true);
    this.errorMessage.set(null);
    this.discoveryService.search(text).subscribe({
      next: (discoveries) => {
        this.discoveries.set(discoveries);
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
