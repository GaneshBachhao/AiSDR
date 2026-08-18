import { Injectable, inject } from '@angular/core';
import { Observable, catchError, forkJoin, map, shareReplay, switchMap, throwError } from 'rxjs';
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

  /** `loadAll()`'s result, cached until `invalidate()` is called -- every
   * screen visit used to re-fetch and re-join all three lists from
   * scratch, even when nothing had changed since the last visit (the
   * "revisit trigger" recorded against the state-management decision in
   * frontend_backlog.md). `shareReplay({ bufferSize: 1, refCount: false })`
   * both replays the last value to any later subscriber (unlike plain
   * `share()`, which only multicasts to subscribers active *during* the
   * original emission) and keeps that value alive across zero-subscriber
   * gaps (i.e. after navigating away). `catchError` clears the cache on
   * failure so a transient network error self-heals on the next call
   * instead of being replayed forever. Callers that mutate a
   * Lead/Company/Contact are responsible for calling `invalidate()`
   * afterward (see LeadForm.save(), LeadDetail.delete()) -- this is a
   * deliberately narrow cache, not a general store: `resolve()` below is
   * intentionally NOT cached, since a detail/edit screen must always see
   * the real current state of the one record it's showing. */
  private cache: Observable<Map<string, LeadDisplay>> | null = null;

  /** Map keyed by lead id, for screens that list many leads at once. */
  loadAll(): Observable<Map<string, LeadDisplay>> {
    if (!this.cache) {
      this.cache = forkJoin({
        leads: this.leadService.list(),
        companies: this.companyService.list(),
        contacts: this.contactService.list(),
      }).pipe(
        map(({ leads, companies, contacts }) => {
          const companyNameById = new Map(companies.map((c) => [c.id, c.name]));
          const contactNameById = new Map(
            contacts.map((c) => [c.id, `${c.first_name} ${c.last_name}`]),
          );
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
        catchError((err) => {
          this.cache = null;
          return throwError(() => err);
        }),
        shareReplay({ bufferSize: 1, refCount: false }),
      );
    }
    return this.cache;
  }

  /** Clear the cached loadAll() result so the next call re-fetches.
   * Call after any create/update/delete of a Lead, Company, or Contact
   * that a cached LeadDisplay could show stale data for. */
  invalidate(): void {
    this.cache = null;
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
