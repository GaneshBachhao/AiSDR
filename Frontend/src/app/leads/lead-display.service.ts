import { Injectable, inject } from '@angular/core';
import { Observable, forkJoin, map, switchMap } from 'rxjs';
import { CompanyService } from '../companies/company.service';
import { ContactService } from '../contacts/contact.service';
import { LeadService } from './lead.service';
import { LeadResponseDTO } from './lead.models';

export interface LeadDisplay {
  lead: LeadResponseDTO;
  companyName: string;
  contactName: string;
}

/**
 * Resolves Lead -> real Company/Contact names via a one-shot triple fetch.
 * Extracted after the second module (Discoveries) needed the exact same
 * "Lead -> Company/Contact" join LeadList already did inline -- see
 * Frontend/docs/frontend_backlog.md EPIC-F06.
 */
@Injectable({ providedIn: 'root' })
export class LeadDisplayService {
  private readonly leadService = inject(LeadService);
  private readonly companyService = inject(CompanyService);
  private readonly contactService = inject(ContactService);

  /** Map keyed by lead id, for screens that list many leads at once. */
  loadAll(): Observable<Map<string, LeadDisplay>> {
    return forkJoin({
      leads: this.leadService.list(),
      companies: this.companyService.list(),
      contacts: this.contactService.list(),
    }).pipe(
      map(({ leads, companies, contacts }) => {
        const companyNameById = new Map(companies.map((c) => [c.id, c.name]));
        const contactNameById = new Map(contacts.map((c) => [c.id, `${c.first_name} ${c.last_name}`]));
        const result = new Map<string, LeadDisplay>();
        for (const lead of leads) {
          result.set(lead.id, {
            lead,
            companyName: companyNameById.get(lead.company_id) ?? 'Unknown company',
            contactName: contactNameById.get(lead.contact_id) ?? 'Unknown contact',
          });
        }
        return result;
      }),
    );
  }

  /** Single-lead resolution for detail/form screens that already know
   * which lead they need, without fetching every lead in the system. */
  resolve(leadId: string): Observable<LeadDisplay> {
    return this.leadService.get(leadId).pipe(
      switchMap((lead) =>
        forkJoin({
          company: this.companyService.get(lead.company_id),
          contact: this.contactService.get(lead.contact_id),
        }).pipe(
          map(({ company, contact }) => ({
            lead,
            companyName: company.name,
            contactName: `${contact.first_name} ${contact.last_name}`,
          })),
        ),
      ),
    );
  }
}
