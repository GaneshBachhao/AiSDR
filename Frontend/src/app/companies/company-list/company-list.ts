import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CompanyService } from '../company.service';
import { CompanyResponseDTO } from '../company.models';

@Component({
  selector: 'app-company-list',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './company-list.html',
  styleUrl: './company-list.scss',
})
export class CompanyList implements OnInit {
  private readonly service = inject(CompanyService);

  protected readonly companies = signal<CompanyResponseDTO[]>([]);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly searchQuery = signal('');

  ngOnInit(): void {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.errorMessage.set(null);
    this.service.list().subscribe({
      next: (companies) => {
        this.companies.set(companies);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load companies. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }

  search(): void {
    const query = this.searchQuery().trim();
    if (!query) {
      this.load();
      return;
    }
    this.loading.set(true);
    this.errorMessage.set(null);
    this.service.search(query).subscribe({
      next: (companies) => {
        this.companies.set(companies);
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
