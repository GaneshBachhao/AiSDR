import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { forkJoin, map, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface DashboardCounts {
  companies: number;
  contacts: number;
  leads: number;
  discoveries: number;
  assessments: number;
  qualifications: number;
  recommendations: number;
}

/**
 * No aggregate/stats endpoint exists in the backend, so these counts come
 * from "how many rows came back on one large page" -- an approximation,
 * not a true total, once any module exceeds its own page size. That size
 * is NOT uniform across routers (verified against the generated
 * src/app/api/schema.d.ts on 2026-08-16, not assumed):
 *
 *  - companies/contacts:            `skip`/`limit`, no upper bound
 *  - leads/discoveries:              `skip`/`limit`, capped at 500
 *  - qualifications:                 `skip`/`limit`, capped at 200
 *  - assessments/recommendations:    `page`/`page_size` (NOT `limit` at
 *    all -- a first version of this service sent `?limit=500` to these
 *    two, which FastAPI silently ignored, undercounting both the moment
 *    either table passes the page_size default of 10), capped at 200
 *
 * Revisit if a real `/stats` endpoint gets added or volumes grow past
 * these caps.
 */
@Injectable({ providedIn: 'root' })
export class DashboardCountsService {
  private readonly http = inject(HttpClient);
  private readonly base = environment.apiBaseUrl;

  load(): Observable<DashboardCounts> {
    const countBySkipLimit = (path: string, limit: number) =>
      this.http
        .get<unknown[]>(`${this.base}${path}`, { params: new HttpParams().set('limit', limit) })
        .pipe(map((items) => items.length));

    const countByPage = (path: string, pageSize: number) =>
      this.http
        .get<unknown[]>(`${this.base}${path}`, {
          params: new HttpParams().set('page', 1).set('page_size', pageSize),
        })
        .pipe(map((items) => items.length));

    return forkJoin({
      companies: countBySkipLimit('/companies', 500),
      contacts: countBySkipLimit('/contacts', 500),
      leads: countBySkipLimit('/leads', 500),
      discoveries: countBySkipLimit('/discoveries', 500),
      assessments: countByPage('/assessments', 200),
      qualifications: countBySkipLimit('/qualifications', 200),
      recommendations: countByPage('/recommendations', 200),
    });
  }
}
