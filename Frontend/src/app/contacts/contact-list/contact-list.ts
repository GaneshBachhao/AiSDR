import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { CompanyService } from '../../companies/company.service';
import { CompanyResponseDTO } from '../../companies/company.models';
import { ContactService } from '../contact.service';
import { ContactResponseDTO } from '../contact.models';

@Component({
  selector: 'app-contact-list',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './contact-list.html',
  styleUrl: './contact-list.scss',
})
export class ContactList implements OnInit {
  private readonly contactService = inject(ContactService);
  private readonly companyService = inject(CompanyService);

  protected readonly contacts = signal<ContactResponseDTO[]>([]);
  private readonly companies = signal<CompanyResponseDTO[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly searchQuery = signal('');

  protected readonly companyNameById = computed(() => {
    const map = new Map<string, string>();
    for (const company of this.companies()) {
      map.set(company.id, company.name);
    }
    return map;
  });

  ngOnInit(): void {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    forkJoin({
      contacts: this.contactService.list(),
      companies: this.companyService.list(),
    }).subscribe({
      next: ({ contacts, companies }) => {
        this.contacts.set(contacts);
        this.companies.set(companies);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load contacts. Check that the API is running.');
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
    this.contactService.search(text).subscribe({
      next: (contacts) => {
        this.contacts.set(contacts);
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
