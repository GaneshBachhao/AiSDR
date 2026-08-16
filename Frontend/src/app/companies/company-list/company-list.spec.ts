import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { CompanyList } from './company-list';
import { CompanyResponseDTO } from '../company.models';

describe('CompanyList', () => {
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/companies`;

  const companies: CompanyResponseDTO[] = [
    {
      id: 'c1',
      name: 'Acme Manufacturing',
      website: null,
      industry: 'Manufacturing',
      company_size: 'Large',
      employee_count: 250,
      country: 'India',
      state: null,
      city: null,
      is_active: true,
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CompanyList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('loads and renders real company rows on init', async () => {
    const fixture = TestBed.createComponent(CompanyList);
    fixture.detectChanges();

    httpMock.expectOne(`${base}?limit=500`).flush(companies);
    await fixture.whenStable();
    fixture.detectChanges();

    const rows = fixture.nativeElement.querySelectorAll('tbody tr');
    expect(rows.length).toBe(1);
    expect(rows[0].textContent).toContain('Acme Manufacturing');
    expect(rows[0].textContent).toContain('Manufacturing');
    expect(rows[0].textContent).toContain('Active');
  });

  it('shows an error message when the list request fails', async () => {
    const fixture = TestBed.createComponent(CompanyList);
    fixture.detectChanges();

    httpMock.expectOne(`${base}?limit=500`).flush('', { status: 500, statusText: 'Server Error' });
    await fixture.whenStable();
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('.error')?.textContent).toContain(
      'Could not load companies',
    );
  });
});
