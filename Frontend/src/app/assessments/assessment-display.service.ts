import { Injectable, inject } from '@angular/core';
import { Observable, forkJoin, map, switchMap } from 'rxjs';
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

  /** Map keyed by assessment id, for screens that list many assessments at once. */
  loadAll(): Observable<Map<string, AssessmentDisplay>> {
    return forkJoin({
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
    );
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
