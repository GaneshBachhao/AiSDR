import { DiscoveryResponseDTO, discoveryCompleteness, discoveryStatusBadgeClass } from './discovery.models';

function discovery(overrides: Partial<DiscoveryResponseDTO> = {}): DiscoveryResponseDTO {
  return {
    id: 'd1',
    lead_id: 'l1',
    problem_statement: null,
    current_solution: null,
    business_impact: null,
    success_criteria: null,
    status: 'CREATED',
    created_at: '2026-08-16T00:00:00Z',
    updated_at: '2026-08-16T00:00:00Z',
    ...overrides,
  };
}

describe('discoveryCompleteness', () => {
  it('counts zero when every needs field is null', () => {
    expect(discoveryCompleteness(discovery())).toEqual({ filled: 0, total: 4 });
  });

  it('counts only the fields that are actually populated', () => {
    const result = discoveryCompleteness(
      discovery({ problem_statement: 'Manual reporting.', business_impact: '12% inefficiency' }),
    );
    expect(result).toEqual({ filled: 2, total: 4 });
  });

  it('does not count a whitespace-only field as filled', () => {
    const result = discoveryCompleteness(discovery({ problem_statement: '   ' }));
    expect(result.filled).toBe(0);
  });

  it('counts all four when every field is populated', () => {
    const result = discoveryCompleteness(
      discovery({
        problem_statement: 'a',
        current_solution: 'b',
        business_impact: 'c',
        success_criteria: 'd',
      }),
    );
    expect(result).toEqual({ filled: 4, total: 4 });
  });
});

describe('discoveryStatusBadgeClass', () => {
  it('maps COMPLETED to badge-ok', () => {
    expect(discoveryStatusBadgeClass('COMPLETED')).toBe('badge-ok');
  });

  it('maps CANCELLED to badge-fail', () => {
    expect(discoveryStatusBadgeClass('CANCELLED')).toBe('badge-fail');
  });

  it('maps IN_PROGRESS to badge-warn', () => {
    expect(discoveryStatusBadgeClass('IN_PROGRESS')).toBe('badge-warn');
  });

  it('maps a freshly-created discovery to the info (blue) badge', () => {
    expect(discoveryStatusBadgeClass('CREATED')).toBe('badge-info');
  });

  it('maps ON_HOLD to badge-neutral', () => {
    expect(discoveryStatusBadgeClass('ON_HOLD')).toBe('badge-neutral');
  });
});
