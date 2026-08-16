import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { ContactList } from './contact-list';
import { ContactResponseDTO } from '../contact.models';
import { CompanyResponseDTO } from '../../companies/company.models';

describe('ContactList', () => {
  let httpMock: HttpTestingController;
  const contactsBase = `${environment.apiBaseUrl}/contacts`;
  const companiesBase = `${environment.apiBaseUrl}/companies`;

  const contacts: ContactResponseDTO[] = [
    {
      id: 'ct1',
      company_id: 'c1',
      first_name: 'Jane',
      last_name: 'Doe',
      email: 'jane@acme.example',
      phone: null,
      job_title: 'COO',
      linkedin_url: null,
      is_active: true,
    },
  ];

  const companies: CompanyResponseDTO[] = [
    {
      id: 'c1',
      name: 'Acme Manufacturing',
      website: null,
      industry: null,
      company_size: null,
      employee_count: null,
      country: null,
      state: null,
      city: null,
      is_active: true,
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContactList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('loads contacts and resolves the company name from a separate companies fetch', async () => {
    const fixture = TestBed.createComponent(ContactList);
    fixture.detectChanges();

    httpMock.expectOne(`${contactsBase}?limit=500`).flush(contacts);
    httpMock.expectOne(`${companiesBase}?limit=500`).flush(companies);
    await fixture.whenStable();
    fixture.detectChanges();

    const row = fixture.nativeElement.querySelector('tbody tr');
    expect(row.textContent).toContain('Jane Doe');
    expect(row.textContent).toContain('Acme Manufacturing');
    expect(row.textContent).toContain('COO');
  });
});
