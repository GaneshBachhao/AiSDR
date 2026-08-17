import { recommendationStatusBadgeClass } from './recommendation.models';

describe('recommendationStatusBadgeClass', () => {
  it('maps Approved to badge-ok', () => {
    expect(recommendationStatusBadgeClass('Approved')).toBe('badge-ok');
  });

  it('maps Rejected to badge-fail', () => {
    expect(recommendationStatusBadgeClass('Rejected')).toBe('badge-fail');
  });

  it('maps Under Review to badge-warn', () => {
    expect(recommendationStatusBadgeClass('Under Review')).toBe('badge-warn');
  });

  it('maps Draft to badge-info', () => {
    expect(recommendationStatusBadgeClass('Draft')).toBe('badge-info');
  });

  it('maps Archived and unrecognized statuses to badge-neutral', () => {
    expect(recommendationStatusBadgeClass('Archived')).toBe('badge-neutral');
    expect(recommendationStatusBadgeClass('Something Else')).toBe('badge-neutral');
  });
});
