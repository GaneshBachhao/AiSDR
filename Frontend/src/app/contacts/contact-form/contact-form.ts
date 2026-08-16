import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CompanyService } from '../../companies/company.service';
import { CompanyResponseDTO } from '../../companies/company.models';
import { ContactService } from '../contact.service';
import { CreateContactRequestDTO, emptyContactForm } from '../contact.models';

@Component({
  selector: 'app-contact-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './contact-form.html',
  styleUrl: './contact-form.scss',
})
export class ContactForm implements OnInit {
  private readonly service = inject(ContactService);
  private readonly companyService = inject(CompanyService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly contactId = signal<string | null>(null);
  protected readonly isEditMode = signal(false);
  protected readonly form = signal<CreateContactRequestDTO>(emptyContactForm());
  protected readonly companies = signal<CompanyResponseDTO[]>([]);
  /** Only known once loaded, and only relevant in edit mode -- Contact's
   * company_id isn't part of UpdateContactRequestDTO, so it's shown for
   * context but can't be changed from this form. */
  protected readonly companyName = signal<string | null>(null);
  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.contactId.set(id);
      this.isEditMode.set(true);
      this.loading.set(true);
      this.service.get(id).subscribe({
        next: (contact) => {
          this.form.set({
            company_id: contact.company_id,
            first_name: contact.first_name,
            last_name: contact.last_name,
            email: contact.email,
            phone: contact.phone ?? null,
            job_title: contact.job_title ?? null,
            linkedin_url: contact.linkedin_url ?? null,
          });
          this.companyService.get(contact.company_id).subscribe({
            next: (company) => this.companyName.set(company.name),
          });
          this.loading.set(false);
        },
        error: () => {
          this.errorMessage.set('Could not load this contact. Check that the API is running.');
          this.loading.set(false);
        },
      });
      return;
    }

    const preselectedCompanyId = this.route.snapshot.queryParamMap.get('company_id') ?? '';
    this.form.set(emptyContactForm(preselectedCompanyId));
    this.companyService.list().subscribe({
      next: (companies) => this.companies.set(companies),
      error: () => this.errorMessage.set('Could not load companies for the picker.'),
    });
  }

  update(field: keyof CreateContactRequestDTO, value: string | null): void {
    this.form.update((f) => ({ ...f, [field]: value === '' ? null : value }));
  }

  save(): void {
    this.saving.set(true);
    this.errorMessage.set(null);
    const id = this.contactId();
    const { company_id, ...updatable } = this.form();

    const request = id ? this.service.update(id, updatable) : this.service.create(this.form());

    request.subscribe({
      next: (contact) => this.router.navigate(['/contacts', contact.id]),
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
