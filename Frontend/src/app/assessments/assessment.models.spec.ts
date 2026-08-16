import { assessmentStatusBadgeClass } from './assessment.models';

describe('assessmentStatusBadgeClass', () => {
  it('maps Completed to badge-ok', () => {
    expect(assessmentStatusBadgeClass('Completed')).toBe('badge-ok');
  });

  it('maps Cancelled to badge-fail', () => {
    expect(assessmentStatusBadgeClass('Cancelled')).toBe('badge-fail');
  });

  it('maps In Progress and Under Review to badge-warn', () => {
    expect(assessmentStatusBadgeClass('In Progress')).toBe('badge-warn');
    expect(assessmentStatusBadgeClass('Under Review')).toBe('badge-warn');
  });

  it('maps Created to badge-info', () => {
    expect(assessmentStatusBadgeClass('Created')).toBe('badge-info');
  });

  it('falls back to badge-neutral for unrecognized statuses', () => {
    expect(assessmentStatusBadgeClass('Something Else')).toBe('badge-neutral');
  });
});
