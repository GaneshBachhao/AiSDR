import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  AssessmentResponseDTO,
  CreateAssessmentRequestDTO,
  UpdateAssessmentRequestDTO,
} from './assessment.models';

/** No /assessments/search endpoint exists (verified against the schema) --
 * list only supports page/page_size/discovery_id, so there's no search
 * bar on this module's list screen, unlike every prior one. */
@Injectable({ providedIn: 'root' })
export class AssessmentService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/assessments`;

  list(): Observable<AssessmentResponseDTO[]> {
    return this.http.get<AssessmentResponseDTO[]>(this.base, {
      params: new HttpParams().set('page', 1).set('page_size', 200),
    });
  }

  get(id: string): Observable<AssessmentResponseDTO> {
    return this.http.get<AssessmentResponseDTO>(`${this.base}/${id}`);
  }

  create(dto: CreateAssessmentRequestDTO): Observable<AssessmentResponseDTO> {
    return this.http.post<AssessmentResponseDTO>(this.base, dto);
  }

  update(id: string, dto: UpdateAssessmentRequestDTO): Observable<AssessmentResponseDTO> {
    return this.http.put<AssessmentResponseDTO>(`${this.base}/${id}`, dto);
  }

  start(id: string): Observable<AssessmentResponseDTO> {
    return this.http.post<AssessmentResponseDTO>(`${this.base}/${id}/start`, {});
  }

  remove(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
