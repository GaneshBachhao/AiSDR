import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  CandidateResearchFailure,
  CompanyResearchBatchResult,
  CompanyResearchRequest,
  CompanySearchResult,
} from './company-research.models';

@Injectable({ providedIn: 'root' })
export class CompanyResearchService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/company-research`;

  search(request: CompanyResearchRequest): Observable<CompanyResearchBatchResult> {
    return this.http.post<CompanyResearchBatchResult>(`${this.baseUrl}/search`, request);
  }

  retry(
    failure: CandidateResearchFailure,
    request: CompanyResearchRequest,
  ): Observable<CompanySearchResult | CandidateResearchFailure | null> {
    return this.http.post<CompanySearchResult | CandidateResearchFailure | null>(
      `${this.baseUrl}/retry`,
      { failure, request },
    );
  }
}
