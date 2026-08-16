import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { LeadDisplayService } from '../../leads/lead-display.service';
import { DiscoveryService } from '../discovery.service';
import { DiscoveryResponseDTO, discoveryCompleteness, discoveryStatusBadgeClass } from '../discovery.models';

@Component({
  selector: 'app-discovery-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './discovery-detail.html',
  styleUrl: './discovery-detail.scss',
})
export class DiscoveryDetail implements OnInit {
  protected readonly discoveryStatusBadgeClass = discoveryStatusBadgeClass;
  protected readonly discoveryCompleteness = discoveryCompleteness;

  private readonly service = inject(DiscoveryService);
  private readonly leadDisplayService = inject(LeadDisplayService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly discovery = signal<DiscoveryResponseDTO | null>(null);
  protected readonly leadId = signal<string | null>(null);
  protected readonly leadLabel = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (discovery) => {
        this.discovery.set(discovery);
        this.leadId.set(discovery.lead_id);
        this.loading.set(false);
        this.leadDisplayService.resolve(discovery.lead_id).subscribe({
          next: ({ companyName, contactName }) => this.leadLabel.set(`${companyName} — ${contactName}`),
        });
      },
      error: () => {
        this.errorMessage.set('Could not load this discovery. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  delete(): void {
    const discovery = this.discovery();
    if (!discovery) return;
    if (!confirm('Delete this discovery? This cannot be undone.')) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(discovery.id).subscribe({
      next: () => this.router.navigate(['/discoveries']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
