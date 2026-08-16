import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

interface NavItem {
  label: string;
  path: string;
}

interface NavGroup {
  heading: string;
  items: NavItem[];
}

/**
 * Sidebar groups mirror the real pipeline dependency order -- verified
 * against the domain code (Qualification requires an assessment_id, so it
 * comes after Assess, not before), not assumed from stage names. See
 * Frontend/docs/design_system.md §2.
 */
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly navGroups: NavGroup[] = [
    {
      heading: 'Discover',
      items: [
        { label: 'Company Research', path: 'company-research' },
        { label: 'Companies', path: 'companies' },
        { label: 'Contacts', path: 'contacts' },
        { label: 'Leads', path: 'leads' },
      ],
    },
    {
      heading: 'Discover Needs',
      items: [{ label: 'Discoveries', path: 'discoveries' }],
    },
    {
      heading: 'Assess',
      items: [{ label: 'Assessments', path: 'assessments' }],
    },
    {
      heading: 'Qualify',
      items: [{ label: 'Qualifications', path: 'qualifications' }],
    },
    {
      heading: 'Recommend',
      items: [{ label: 'Recommendations', path: 'recommendations' }],
    },
    {
      heading: 'Act',
      items: [{ label: 'Actions', path: 'actions' }],
    },
  ];
}
