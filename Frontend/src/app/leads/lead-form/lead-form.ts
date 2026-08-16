import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CompanyService } from '../../companies/company.service';
import { CompanyResponseDTO } from '../../companies/company.models';
import { ContactService } from '../../contacts/contact.service';
import { ContactResponseDTO } from '../../contacts/contact.models';
import { LeadService } from '../lead.service';
import {
  CreateLeadRequestDTO,
  LEAD_SOURCES,
  LEAD_STATUSES,
  LeadStatus,
  emptyLeadForm,
} from '../lead.models';

@Component({
  selector: 'app-lead-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './lead-form.html',
  styleUrl: './lead-form.scss',
})
export class LeadForm implements OnInit {
  private readonly service = inject(LeadService);
  private readonly companyService = inject(CompanyService);
  private readonly contactService = inject(ContactService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly sources = LEAD_SOURCES;
  protected readonly statuses = LEAD_STATUSES;

  protected readonly leadId = signal<string | null>(null);
  protected readonly isEditMode = signal(false);
  protected readonly form = signal<CreateLeadRequestDTO>(emptyLeadForm());
  protected readonly status = signal<LeadStatus>('New');
  protected readonly companyName = signal<string | null>(null);

  protected readonly companies = signal<CompanyResponseDTO[]>([]);
  private readonly allContacts = signal<ContactResponseDTO[]>([]);
  /** Filtered to the selected company -- the backend rejects a Lead whose
   * Contact doesn't belong to its Company, so the picker only offers
   * valid combinations instead of letting the request fail. */
  protected readonly contactsForSelectedCompany = computed(() =>
    this.allContacts().filter((c) => c.company_id === this.form().company_id),
  );

  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.contactService.list().subscribe({ next: (contacts) => this.allContacts.set(contacts) });

    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.leadId.set(id);
      this.isEditMode.set(true);
      this.loading.set(true);
      this.service.get(id).subscribe({
        next: (lead) => {
          this.form.set({
            company_id: lead.company_id,
            contact_id: lead.contact_id,
            source: lead.source,
            score: lead.score,
            notes: lead.notes ?? null,
          });
          this.status.set(lead.status);
          this.companyService.get(lead.company_id).subscribe({
            next: (company) => this.companyName.set(company.name),
          });
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('Could not load this lead. Check that the API is running.');
          this.loading.set(false);
        },
      });
      return;
    }

    const params = this.route.snapshot.queryParamMap;
    this.form.set(emptyLeadForm(params.get('company_id') ?? '', params.get('contact_id') ?? ''));
    this.companyService.list().subscribe({
      next: (companies) => this.companies.set(companies),
      error: () => this.errorMessage.set('Could not load companies for the picker.'),
    });
  }

  updateForm<K extends keyof CreateLeadRequestDTO>(field: K, value: CreateLeadRequestDTO[K]): void {
    this.form.update((f) => ({ ...f, [field]: value }));
  }

  onCompanyChange(companyId: string): void {
    // Changing the company invalidates any previously-picked contact from
    // a different company.
    this.form.update((f) => ({ ...f, company_id: companyId, contact_id: '' }));
  }

  save(): void {
    this.saving.set(true);
    this.errorMessage.set(null);
    const id = this.leadId();

    const request = id
      ? this.service.update(id, {
          contact_id: this.form().contact_id,
          source: this.form().source,
          status: this.status(),
          score: this.form().score,
          notes: this.form().notes,
        })
      : this.service.create(this.form());

    request.subscribe({
      next: (lead) => this.router.navigate(['/leads', lead.id]),
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
