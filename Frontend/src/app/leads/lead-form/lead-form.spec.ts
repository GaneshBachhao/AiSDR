import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { provideRouter } from '@angular/router';
import { environment } from '../../../environments/environment';
import { LeadForm } from './lead-form';
import { ContactResponseDTO } from '../../contacts/contact.models';

describe('LeadForm', () => {
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
      job_title: null,
      linkedin_url: null,
      is_active: true,
    },
    {
      id: 'ct2',
      company_id: 'c2',
      first_name: 'John',
      last_name: 'Smith',
      email: 'john@other.example',
      phone: null,
      job_title: null,
      linkedin_url: null,
      is_active: true,
    },
  ];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LeadForm],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: new Map(), queryParamMap: new Map() } } },
      ],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('only offers contacts belonging to the currently-selected company', async () => {
    const fixture = TestBed.createComponent(LeadForm);
    const component = fixture.componentInstance;
    fixture.detectChanges();

    httpMock.expectOne(`${contactsBase}?limit=500`).flush(contacts);
    httpMock.expectOne(`${companiesBase}?limit=500`).flush([]);
    await fixture.whenStable();

    expect(component['contactsForSelectedCompany']()).toEqual([]);

    component.onCompanyChange('c1');
    const forC1 = component['contactsForSelectedCompany']();
    expect(forC1.length).toBe(1);
    expect(forC1[0].id).toBe('ct1');

    component.onCompanyChange('c2');
    const forC2 = component['contactsForSelectedCompany']();
    expect(forC2.length).toBe(1);
    expect(forC2[0].id).toBe('ct2');
  });

  it('clears the previously-picked contact when the company changes', async () => {
    const fixture = TestBed.createComponent(LeadForm);
    const component = fixture.componentInstance;
    fixture.detectChanges();

    httpMock.expectOne(`${contactsBase}?limit=500`).flush(contacts);
    httpMock.expectOne(`${companiesBase}?limit=500`).flush([]);
    await fixture.whenStable();

    component.onCompanyChange('c1');
    component.updateForm('contact_id', 'ct1');
    expect(component['form']().contact_id).toBe('ct1');

    component.onCompanyChange('c2');
    expect(component['form']().contact_id).toBe('');
  });
});
