import { emptyQualificationForm, qualificationStatusBadgeClass } from './qualification.models';

describe('qualificationStatusBadgeClass', () => {
  it('maps Qualified to badge-ok', () => {
    expect(qualificationStatusBadgeClass('Qualified')).toBe('badge-ok');
  });

  it('maps Disqualified to badge-fail', () => {
    expect(qualificationStatusBadgeClass('Disqualified')).toBe('badge-fail');
  });

  it('maps Partially Qualified to badge-warn', () => {
    expect(qualificationStatusBadgeClass('Partially Qualified')).toBe('badge-warn');
  });

  it('maps Needs Nurturing to badge-info', () => {
    expect(qualificationStatusBadgeClass('Needs Nurturing')).toBe('badge-info');
  });

  it('falls back to badge-neutral for unrecognized statuses', () => {
    expect(qualificationStatusBadgeClass('Something Else')).toBe('badge-neutral');
  });
});

describe('emptyQualificationForm', () => {
  it('defaults to Partially Qualified with score 0, matching the domain default', () => {
    expect(emptyQualificationForm()).toEqual({
      lead_id: '',
      assessment_id: '',
      status: 'Partially Qualified',
      score: 0,
      recommendation: null,
    });
  });

  it('accepts a preselected lead and assessment id', () => {
    expect(emptyQualificationForm('l1', 'a1')).toEqual(
      expect.objectContaining({ lead_id: 'l1', assessment_id: 'a1' }),
    );
  });
});
