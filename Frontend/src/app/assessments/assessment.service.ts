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

  /** A Discovery has at most one Assessment -- enforced by a unique
   * constraint on discovery_id at the persistence layer (verified in
   * Backend/app/infrastructure/persistence/models/assessment_model.py),
   * though unlike Discovery's own one-per-Lead rule it isn't mapped to a
   * clean 409; a duplicate create surfaces as a raw 500 instead (a
   * backend gap, not fixed here -- see frontend_backlog.md EPIC-F10). */
  listByDiscovery(discoveryId: string): Observable<AssessmentResponseDTO[]> {
    return this.http.get<AssessmentResponseDTO[]>(this.base, {
      params: new HttpParams().set('page', 1).set('page_size', 1).set('discovery_id', discoveryId),
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
