import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { App } from './app';
import { routes } from './app.routes';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter(routes)],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('renders a sidebar link for every module, in the real pipeline order', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    await fixture.whenStable();
    const links = fixture.nativeElement.querySelectorAll('.sidebar a');
    const labels = Array.from(links).map((el) => (el as HTMLElement).textContent?.trim());
    expect(labels).toEqual([
      'Command Center',
      'Company Research',
      'Companies',
      'Contacts',
      'Leads',
      'Discoveries',
      'Assessments',
      'Qualifications',
      'Recommendations',
      'Actions',
      'Admin',
    ]);
  });

  it('groups nav links under headings that match the real pipeline stages', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    await fixture.whenStable();
    const headings = fixture.nativeElement.querySelectorAll('.nav-heading');
    const labels = Array.from(headings).map((el) => (el as HTMLElement).textContent?.trim());
    expect(labels).toEqual([
      'Discover',
      'Discover Needs',
      'Assess',
      'Qualify',
      'Recommend',
      'Act',
    ]);
  });
});
