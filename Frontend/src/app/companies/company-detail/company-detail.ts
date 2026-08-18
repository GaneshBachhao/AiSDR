import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { ContactService } from '../../contacts/contact.service';
import { ContactResponseDTO } from '../../contacts/contact.models';
import { DiscoveryService } from '../../discoveries/discovery.service';
import {
  DiscoveryResponseDTO,
  discoveryStatusBadgeClass,
} from '../../discoveries/discovery.models';
import { LeadService } from '../../leads/lead.service';
import { LeadResponseDTO, leadStatusBadgeClass } from '../../leads/lead.models';
import { CompanyService } from '../company.service';
import { CompanyResponseDTO } from '../company.models';

@Component({
  selector: 'app-company-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './company-detail.html',
  styleUrl: './company-detail.scss',
})
export class CompanyDetail implements OnInit {
  protected readonly leadStatusBadgeClass = leadStatusBadgeClass;
  protected readonly discoveryStatusBadgeClass = discoveryStatusBadgeClass;

  private readonly service = inject(CompanyService);
  private readonly contactService = inject(ContactService);
  private readonly leadService = inject(LeadService);
  private readonly discoveryService = inject(DiscoveryService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly company = signal<CompanyResponseDTO | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  // Cross-entity drill-down (EPIC-F10): Contact/Discovery have no
  // company_id filter server-side, so those two are fetched in full and
  // filtered client-side; Lead's list endpoint does support company_id,
  // so that one goes straight to the server.
  protected readonly contacts = signal<ContactResponseDTO[]>([]);
  protected readonly leads = signal<LeadResponseDTO[]>([]);
  protected readonly discoveries = signal<DiscoveryResponseDTO[]>([]);
  private readonly contactNameById = signal<Map<string, string>>(new Map());
  protected readonly relatedLoading = signal(true);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  protected contactNameFor(contactId: string): string {
    return this.contactNameById().get(contactId) ?? 'Unknown contact';
  }

  protected discoveryLeadContact(discovery: DiscoveryResponseDTO): string {
    const lead = this.leads().find((l) => l.id === discovery.lead_id);
    return lead ? this.contactNameFor(lead.contact_id) : 'Unknown lead';
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (company) => {
        this.company.set(company);
        this.loading.set(false);
        this.loadRelated(company.id);
      },
      error: () => {
        this.errorMessage.set('Could not load this company. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  private loadRelated(companyId: string): void {
    forkJoin({
      contacts: this.contactService.list(),
      leads: this.leadService.listByCompany(companyId),
      discoveries: this.discoveryService.list(),
    }).subscribe({
      next: ({ contacts, leads, discoveries }) => {
        const companyContacts = contacts.filter((c) => c.company_id === companyId);
        this.contacts.set(companyContacts);
        this.contactNameById.set(
          new Map(contacts.map((c) => [c.id, `${c.first_name} ${c.last_name}`])),
        );
        this.leads.set(leads);
        const leadIds = new Set(leads.map((l) => l.id));
        this.discoveries.set(discoveries.filter((d) => leadIds.has(d.lead_id)));
        this.relatedLoading.set(false);
      },
      error: () => {
        this.relatedLoading.set(false);
      },
    });
  }

  delete(): void {
    const company = this.company();
    if (!company) return;
    if (!confirm(`Delete "${company.name}"? This cannot be undone.`)) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(company.id).subscribe({
      next: () => this.router.navigate(['/companies']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
