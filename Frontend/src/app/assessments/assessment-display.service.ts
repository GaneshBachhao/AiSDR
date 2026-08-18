import { Injectable, inject } from '@angular/core';
import { Observable, catchError, forkJoin, map, shareReplay, switchMap, throwError } from 'rxjs';
import { DiscoveryService } from '../discoveries/discovery.service';
import { AssessmentService } from './assessment.service';
import { AssessmentResponseDTO } from './assessment.models';

export interface AssessmentDisplay {
  assessment: AssessmentResponseDTO;
  discoveryLabel: string;
}

/**
 * Resolves Assessment -> its Discovery's problem statement, via a one-shot
 * join. Extracted after the second module (Qualification) needed the same
 * "Assessment -> Discovery" lookup AssessmentList already did inline --
 * see Frontend/docs/frontend_backlog.md EPIC-F09, mirroring the precedent
 * LeadDisplayService set in EPIC-F06.
 */
@Injectable({ providedIn: 'root' })
export class AssessmentDisplayService {
  private readonly assessmentService = inject(AssessmentService);
  private readonly discoveryService = inject(DiscoveryService);

  private static labelFor(problemStatement: string | null | undefined): string {
    return problemStatement ?? 'Discovery (no problem statement captured)';
  }

  /** `loadAll()`'s result, cached until `invalidate()` is called -- same
   * rationale and caching shape as LeadDisplayService.loadAll() (see its
   * own comment for why `shareReplay` + `catchError`, not plain `share`).
   * Callers that mutate an Assessment or Discovery are responsible for
   * calling `invalidate()` afterward (see AssessmentForm.save(),
   * AssessmentDetail.delete()/start()). `resolve()` stays uncached for
   * the same reason LeadDisplayService.resolve() does. */
  private cache: Observable<Map<string, AssessmentDisplay>> | null = null;

  /** Map keyed by assessment id, for screens that list many assessments at once. */
  loadAll(): Observable<Map<string, AssessmentDisplay>> {
    if (!this.cache) {
      this.cache = forkJoin({
        assessments: this.assessmentService.list(),
        discoveries: this.discoveryService.list(),
      }).pipe(
        map(({ assessments, discoveries }) => {
          const discoveryById = new Map(discoveries.map((d) => [d.id, d]));
          const result = new Map<string, AssessmentDisplay>();
          for (const assessment of assessments) {
            result.set(assessment.assessment_id, {
              assessment,
              discoveryLabel: AssessmentDisplayService.labelFor(
                discoveryById.get(assessment.discovery_id)?.problem_statement,
              ),
            });
          }
          return result;
        }),
        catchError((err) => {
          this.cache = null;
          return throwError(() => err);
        }),
        shareReplay({ bufferSize: 1, refCount: false }),
      );
    }
    return this.cache;
  }

  /** Clear the cached loadAll() result so the next call re-fetches.
   * Call after any create/update/delete/start of an Assessment, or a
   * create/update/delete of a Discovery, that a cached AssessmentDisplay
   * could show stale data for. */
  invalidate(): void {
    this.cache = null;
  }

  /** Single-assessment resolution for detail/form screens that already
   * know which assessment they need, without fetching every assessment. */
  resolve(assessmentId: string): Observable<AssessmentDisplay> {
    return this.assessmentService.get(assessmentId).pipe(
      switchMap((assessment) =>
        this.discoveryService.get(assessment.discovery_id).pipe(
          map((discovery) => ({
            assessment,
            discoveryLabel: AssessmentDisplayService.labelFor(discovery.problem_statement),
          })),
        ),
      ),
    );
  }
}
