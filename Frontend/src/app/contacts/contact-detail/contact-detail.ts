import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CompanyService } from '../../companies/company.service';
import { ContactService } from '../contact.service';
import { ContactResponseDTO } from '../contact.models';

@Component({
  selector: 'app-contact-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './contact-detail.html',
  styleUrl: './contact-detail.scss',
})
export class ContactDetail implements OnInit {
  private readonly service = inject(ContactService);
  private readonly companyService = inject(CompanyService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly contact = signal<ContactResponseDTO | null>(null);
  protected readonly companyId = signal<string | null>(null);
  protected readonly companyName = signal<string | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (contact) => {
        this.contact.set(contact);
        this.companyId.set(contact.company_id);
        this.loading.set(false);
        this.companyService.get(contact.company_id).subscribe({
          next: (company) => this.companyName.set(company.name),
        });
      },
      error: () => {
        this.errorMessage.set('Could not load this contact. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  delete(): void {
    const contact = this.contact();
    if (!contact) return;
    if (!confirm(`Delete ${contact.first_name} ${contact.last_name}? This cannot be undone.`)) {
      return;
    }
    this.deleting.set(true);
    this.service.remove(contact.id).subscribe({
      next: () => this.router.navigate(['/contacts']),
      error: () => {
        this.errorMessage.set('Delete failed. Check that the API is running.');
        this.deleting.set(false);
      },
    });
  }
}
