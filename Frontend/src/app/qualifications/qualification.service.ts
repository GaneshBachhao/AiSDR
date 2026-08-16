import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  CreateQualificationRequestDTO,
  QualificationResponseDTO,
  UpdateQualificationRequestDTO,
} from './qualification.models';

/** No /qualifications/search endpoint exists, same as Assessment -- list
 * only supports skip/limit/lead_id/assessment_id (verified against
 * qualification_router.py); limit is capped at 200 (le=200). */
@Injectable({ providedIn: 'root' })
export class QualificationService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/qualifications`;

  list(): Observable<QualificationResponseDTO[]> {
    return this.http.get<QualificationResponseDTO[]>(this.base, {
      params: new HttpParams().set('skip', 0).set('limit', 200),
    });
  }

  get(id: string): Observable<QualificationResponseDTO> {
    return this.http.get<QualificationResponseDTO>(`${this.base}/${id}`);
  }

  create(dto: CreateQualificationRequestDTO): Observable<QualificationResponseDTO> {
    return this.http.post<QualificationResponseDTO>(this.base, dto);
  }

  update(id: string, dto: UpdateQualificationRequestDTO): Observable<QualificationResponseDTO> {
    return this.http.put<QualificationResponseDTO>(`${this.base}/${id}`, dto);
  }

  remove(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
