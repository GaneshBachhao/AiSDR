import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { CreateLeadRequestDTO, LeadResponseDTO, UpdateLeadRequestDTO } from './lead.models';

/** Note: /leads/search uses `keyword` -- Company uses `query`, Contact uses
 * `search_text`. Three modules, three different param names so far; keep
 * checking the generated schema per-router, don't assume. */
@Injectable({ providedIn: 'root' })
export class LeadService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/leads`;

  list(): Observable<LeadResponseDTO[]> {
    return this.http.get<LeadResponseDTO[]>(this.base, {
      params: new HttpParams().set('limit', 500),
    });
  }

  /** Unlike Contact/Discovery, Lead's list endpoint does support a
   * company_id filter server-side (verified in
   * Backend/app/presentation/api/routers/lead_router.py). */
  listByCompany(companyId: string): Observable<LeadResponseDTO[]> {
    return this.http.get<LeadResponseDTO[]>(this.base, {
      params: new HttpParams().set('company_id', companyId).set('limit', 500),
    });
  }

  search(keyword: string): Observable<LeadResponseDTO[]> {
    return this.http.get<LeadResponseDTO[]>(`${this.base}/search`, {
      params: new HttpParams().set('keyword', keyword).set('limit', 500),
    });
  }

  get(id: string): Observable<LeadResponseDTO> {
    return this.http.get<LeadResponseDTO>(`${this.base}/${id}`);
  }

  create(dto: CreateLeadRequestDTO): Observable<LeadResponseDTO> {
    return this.http.post<LeadResponseDTO>(this.base, dto);
  }

  update(id: string, dto: UpdateLeadRequestDTO): Observable<LeadResponseDTO> {
    return this.http.put<LeadResponseDTO>(`${this.base}/${id}`, dto);
  }

  remove(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
