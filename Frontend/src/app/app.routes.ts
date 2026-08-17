import { Routes } from '@angular/router';
import { Admin } from './admin/admin';
import { authGuard } from './auth/auth.guard';
import { Login } from './auth/login/login';
import { AssessmentDetail } from './assessments/assessment-detail/assessment-detail';
import { AssessmentForm } from './assessments/assessment-form/assessment-form';
import { AssessmentList } from './assessments/assessment-list/assessment-list';
import { CommandCenter } from './command-center/command-center';
import { CompanyDetail } from './companies/company-detail/company-detail';
import { CompanyForm } from './companies/company-form/company-form';
import { CompanyList } from './companies/company-list/company-list';
import { CompanyResearch } from './company-research/company-research';
import { ContactDetail } from './contacts/contact-detail/contact-detail';
import { ContactForm } from './contacts/contact-form/contact-form';
import { ContactList } from './contacts/contact-list/contact-list';
import { DiscoveryDetail } from './discoveries/discovery-detail/discovery-detail';
import { DiscoveryForm } from './discoveries/discovery-form/discovery-form';
import { DiscoveryList } from './discoveries/discovery-list/discovery-list';
import { LeadDetail } from './leads/lead-detail/lead-detail';
import { LeadForm } from './leads/lead-form/lead-form';
import { LeadList } from './leads/lead-list/lead-list';
import { QualificationDetail } from './qualifications/qualification-detail/qualification-detail';
import { QualificationForm } from './qualifications/qualification-form/qualification-form';
import { QualificationList } from './qualifications/qualification-list/qualification-list';
import { RecommendationDetail } from './recommendations/recommendation-detail/recommendation-detail';
import { RecommendationForm } from './recommendations/recommendation-form/recommendation-form';
import { RecommendationList } from './recommendations/recommendation-list/recommendation-list';
import { ComingSoon } from './shared/coming-soon/coming-soon';

/**
 * One named route per backend module (Frontend/docs/frontend_backlog.md
 * EPIC-F01), grouped by the real pipeline order (Frontend/docs/
 * design_system.md §2), even before each screen has a real component --
 * stub routes point at the shared ComingSoon placeholder until their epic
 * ships. Command Center (not Company Research) is now the landing page.
 */
export const routes: Routes = [
  { path: 'login', component: Login },

  {
    path: '',
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'command-center', pathMatch: 'full' },
      { path: 'command-center', component: CommandCenter },

      { path: 'company-research', component: CompanyResearch, data: { title: 'Company Research' } },
      { path: 'companies', component: CompanyList },
      { path: 'companies/new', component: CompanyForm },
      { path: 'companies/:id', component: CompanyDetail },
      { path: 'companies/:id/edit', component: CompanyForm },
      { path: 'contacts', component: ContactList },
      { path: 'contacts/new', component: ContactForm },
      { path: 'contacts/:id', component: ContactDetail },
      { path: 'contacts/:id/edit', component: ContactForm },
      { path: 'leads', component: LeadList },
      { path: 'leads/new', component: LeadForm },
      { path: 'leads/:id', component: LeadDetail },
      { path: 'leads/:id/edit', component: LeadForm },

      { path: 'discoveries', component: DiscoveryList },
      { path: 'discoveries/new', component: DiscoveryForm },
      { path: 'discoveries/:id', component: DiscoveryDetail },
      { path: 'discoveries/:id/edit', component: DiscoveryForm },
      { path: 'assessments', component: AssessmentList },
      { path: 'assessments/new', component: AssessmentForm },
      { path: 'assessments/:id', component: AssessmentDetail },
      { path: 'assessments/:id/edit', component: AssessmentForm },
      { path: 'qualifications', component: QualificationList },
      { path: 'qualifications/new', component: QualificationForm },
      { path: 'qualifications/:id', component: QualificationDetail },
      { path: 'qualifications/:id/edit', component: QualificationForm },
      { path: 'recommendations', component: RecommendationList },
      { path: 'recommendations/new', component: RecommendationForm },
      { path: 'recommendations/:id', component: RecommendationDetail },
      { path: 'actions', component: ComingSoon, data: { title: 'Actions' } },

      { path: 'admin', component: Admin },
    ],
  },
];
