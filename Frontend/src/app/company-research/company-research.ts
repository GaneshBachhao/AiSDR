import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CompanyResearchService } from './company-research.service';
import {
  CandidateResearchFailure,
  CompanyResearchRequest,
  CompanySearchResult,
  defaultCompanyResearchRequest,
} from './company-research.models';

/** Comma-separated text the form edits, kept separate from the typed
 * request arrays so the input can hold a trailing comma/space while typing. */
interface FormState {
  industriesText: string;
  companySizeText: string;
  servicesText: string;
}

@Component({
  selector: 'app-company-research',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './company-research.html',
  styleUrl: './company-research.scss',
})
export class CompanyResearch {
  private readonly service = inject(CompanyResearchService);

  readonly request = signal<CompanyResearchRequest>(defaultCompanyResearchRequest());
  readonly form = signal<FormState>({ industriesText: '', companySizeText: '', servicesText: '' });

  readonly loading = signal(false);
  readonly errorMessage = signal<string | null>(null);
  readonly results = signal<CompanySearchResult[]>([]);
  readonly failures = signal<CandidateResearchFailure[]>([]);
  readonly retryingCompany = signal<string | null>(null);

  private static splitList(value: string): string[] {
    return value
      .split(',')
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
  }

  search(): void {
    const form = this.form();
    const req: CompanyResearchRequest = {
      ...this.request(),
      industries: CompanyResearch.splitList(form.industriesText),
      company_size: CompanyResearch.splitList(form.companySizeText),
      services: CompanyResearch.splitList(form.servicesText),
    };
    this.request.set(req);

    this.loading.set(true);
    this.errorMessage.set(null);
    this.results.set([]);
    this.failures.set([]);

    this.service.search(req).subscribe({
      next: (batch) => {
        this.results.set(batch.results);
        this.failures.set(batch.failures);
        this.loading.set(false);
      },
      error: (err) => {
        this.errorMessage.set(this.describeError(err));
        this.loading.set(false);
      },
    });
  }

  retry(failure: CandidateResearchFailure): void {
    this.retryingCompany.set(failure.company_name);
    this.errorMessage.set(null);

    this.service.retry(failure, this.request()).subscribe({
      next: (outcome) => {
        this.failures.update((items) =>
          items.filter((item) => item !== failure),
        );
        if (outcome && 'qualification_score' in outcome) {
          this.results.update((items) => [...items, outcome as CompanySearchResult]);
        } else if (outcome && 'failed_step' in outcome) {
          this.failures.update((items) => [...items, outcome as CandidateResearchFailure]);
        }
        // outcome === null: candidate no longer qualifies -- correctly
        // dropped, not shown anywhere, same as a fresh search would do.
        this.retryingCompany.set(null);
      },
      error: (err) => {
        this.errorMessage.set(this.describeError(err));
        this.retryingCompany.set(null);
      },
    });
  }

  private describeError(err: unknown): string {
    if (err && typeof err === 'object' && 'error' in err) {
      const body = (err as { error?: { detail?: string } }).error;
      if (body?.detail) {
        return body.detail;
      }
    }
    return 'Company research request failed. Check that the API is running.';
  }
}
