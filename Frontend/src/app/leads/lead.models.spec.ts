import { leadStatusBadgeClass } from './lead.models';

describe('leadStatusBadgeClass', () => {
  it('maps positive outcomes to badge-ok', () => {
    expect(leadStatusBadgeClass('Qualified')).toBe('badge-ok');
    expect(leadStatusBadgeClass('Converted')).toBe('badge-ok');
  });

  it('maps a negative outcome to badge-fail', () => {
    expect(leadStatusBadgeClass('Disqualified')).toBe('badge-fail');
  });

  it('maps an in-progress state to badge-warn', () => {
    expect(leadStatusBadgeClass('Contacted')).toBe('badge-warn');
  });

  it('maps a fresh lead to the info (blue) badge, not the washed-out neutral one', () => {
    expect(leadStatusBadgeClass('New')).toBe('badge-info');
  });

  it('maps a terminal state to badge-neutral', () => {
    expect(leadStatusBadgeClass('Closed')).toBe('badge-neutral');
  });
});
