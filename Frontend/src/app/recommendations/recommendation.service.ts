import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { GenerateRecommendationRequestDTO, RecommendationResponseDTO } from './recommendation.models';

/** No update or delete endpoint exists -- Recommendations are AI-generated
 * and read-mostly by design (verified against recommendation_router.py,
 * which only wires POST/GET/GET {id}). `create()` is really "generate": the
 * backend is idempotent per assessment_id, returning the existing
 * Recommendation instead of creating a duplicate if one already exists for
 * that assessment. */
@Injectable({ providedIn: 'root' })
export class RecommendationService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/recommendations`;

  list(): Observable<RecommendationResponseDTO[]> {
    return this.http.get<RecommendationResponseDTO[]>(this.base, {
      params: new HttpParams().set('page', 1).set('page_size', 200),
    });
  }

  get(id: string): Observable<RecommendationResponseDTO> {
    return this.http.get<RecommendationResponseDTO>(`${this.base}/${id}`);
  }

  generate(dto: GenerateRecommendationRequestDTO): Observable<RecommendationResponseDTO> {
    return this.http.post<RecommendationResponseDTO>(this.base, dto);
  }
}
