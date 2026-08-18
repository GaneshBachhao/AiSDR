import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { ContactService } from './contact.service';
import { ContactResponseDTO } from './contact.models';

describe('ContactService', () => {
  let service: ContactService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/contacts`;

  const sample: ContactResponseDTO = {
    id: 'ct1',
    company_id: 'c1',
    first_name: 'Jane',
    last_name: 'Doe',
    email: 'jane@acme.example',
    phone: null,
    job_title: null,
    linkedin_url: null,
    is_active: true,
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ContactService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('lists contacts with a generous limit', () => {
    service.list().subscribe();
    const req = httpMock.expectOne(`${base}?limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('searches contacts using search_text, not query', () => {
    service.search('jane').subscribe();
    const req = httpMock.expectOne(`${base}/search?search_text=jane&limit=500`);
    expect(req.request.method).toBe('GET');
    req.flush([sample]);
  });

  it('gets a single contact by id', () => {
    service.get('ct1').subscribe();
    const req = httpMock.expectOne(`${base}/ct1`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });

  it('creates a contact', () => {
    service
      .create({
        company_id: 'c1',
        first_name: 'Jane',
        last_name: 'Doe',
        email: 'jane@acme.example',
      })
      .subscribe();
    const req = httpMock.expectOne(base);
    expect(req.request.method).toBe('POST');
    req.flush(sample);
  });

  it('updates a contact', () => {
    service.update('ct1', { job_title: 'COO' }).subscribe();
    const req = httpMock.expectOne(`${base}/ct1`);
    expect(req.request.method).toBe('PUT');
    req.flush(sample);
  });

  it('deletes a contact', () => {
    service.remove('ct1').subscribe();
    const req = httpMock.expectOne(`${base}/ct1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
