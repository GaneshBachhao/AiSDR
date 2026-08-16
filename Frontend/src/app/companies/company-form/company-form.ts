import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CompanyService } from '../company.service';
import { CreateCompanyRequestDTO, emptyCompanyForm } from '../company.models';

@Component({
  selector: 'app-company-form',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './company-form.html',
  styleUrl: './company-form.scss',
})
export class CompanyForm implements OnInit {
  private readonly service = inject(CompanyService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly companyId = signal<string | null>(null);
  protected readonly isEditMode = signal(false);
  protected readonly form = signal<CreateCompanyRequestDTO>(emptyCompanyForm());
  protected readonly loading = signal(false);
  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      return;
    }
    this.companyId.set(id);
    this.isEditMode.set(true);
    this.loading.set(true);
    this.service.get(id).subscribe({
      next: (company) => {
        this.form.set({
          name: company.name,
          website: company.website ?? null,
          industry: company.industry ?? null,
          company_size: company.company_size ?? null,
          employee_count: company.employee_count ?? null,
          country: company.country ?? null,
          state: company.state ?? null,
          city: company.city ?? null,
        });
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load this company. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  update(field: keyof CreateCompanyRequestDTO, value: string | number | null): void {
    this.form.update((f) => ({ ...f, [field]: value === '' ? null : value }));
  }

  save(): void {
    this.saving.set(true);
    this.errorMessage.set(null);
    const id = this.companyId();

    const request = id ? this.service.update(id, this.form()) : this.service.create(this.form());

    request.subscribe({
      next: (company) => {
        this.router.navigate(['/companies', company.id]);
      },
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
