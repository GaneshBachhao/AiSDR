import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

/**
 * Generic placeholder for a module route that has a nav entry and a real
 * backend router behind it, but no screen built yet -- see
 * Frontend/docs/frontend_backlog.md EPIC-F01 ("route structure supports
 * the rest of this backlog, even before each screen is built"). Reads its
 * title from route data rather than being duplicated per module.
 */
@Component({
  selector: 'app-coming-soon',
  standalone: true,
  template: `
    <div class="coming-soon">
      <h1>{{ title }}</h1>
      <p>This screen isn't built yet -- see Frontend/docs/frontend_backlog.md for its epic.</p>
    </div>
  `,
  styles: [
    `
      .coming-soon {
        max-width: 1100px;
        margin: 0 auto;
        padding: 60px 20px;
        text-align: center;
        color: var(--color-ink-soft);
      }

      h1 {
        color: var(--color-ink);
        margin-bottom: 8px;
        font-size: 20px;
      }
    `,
  ],
})
export class ComingSoon {
  private readonly route = inject(ActivatedRoute);
  protected readonly title = this.route.snapshot.data['title'] ?? 'Coming soon';
}
