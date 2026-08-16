import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
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
  private readonly service = inject(CompanyService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  protected readonly company = signal<CompanyResponseDTO | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);
  protected readonly deleting = signal(false);

  private get id(): string {
    return this.route.snapshot.paramMap.get('id')!;
  }

  ngOnInit(): void {
    this.service.get(this.id).subscribe({
      next: (company) => {
        this.company.set(company);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load this company. Check that the API is running.');
        this.loading.set(false);
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
