import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { vi } from 'vitest';
import { environment } from '../../environments/environment';
import { authInterceptor } from './auth.interceptor';
import { AuthService } from './auth.service';

describe('authInterceptor', () => {
  let http: HttpClient;
  let httpMock: HttpTestingController;
  let authService: AuthService;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptors([authInterceptor])),
        provideHttpClientTesting(),
        provideRouter([]),
      ],
    });
    http = TestBed.inject(HttpClient);
    httpMock = TestBed.inject(HttpTestingController);
    authService = TestBed.inject(AuthService);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('attaches Authorization: Bearer <token> to a request with a stored token', () => {
    localStorage.setItem('aisdr_access_token', 'stored-token');

    http.get(`${environment.apiBaseUrl}/companies`).subscribe();

    const req = httpMock.expectOne(`${environment.apiBaseUrl}/companies`);
    expect(req.request.headers.get('Authorization')).toBe('Bearer stored-token');
    req.flush([]);
  });

  it('does not attach a header when there is no stored token', () => {
    http.get(`${environment.apiBaseUrl}/companies`).subscribe();

    const req = httpMock.expectOne(`${environment.apiBaseUrl}/companies`);
    expect(req.request.headers.has('Authorization')).toBe(false);
    req.flush([]);
  });

  it('logs out and still propagates the error on a 401 from the API', () => {
    localStorage.setItem('aisdr_access_token', 'stale-token');
    const logoutSpy = vi.spyOn(authService, 'logout').mockImplementation(() => {});

    let observedError: unknown;
    http.get(`${environment.apiBaseUrl}/companies`).subscribe({
      error: (err) => (observedError = err),
    });

    httpMock
      .expectOne(`${environment.apiBaseUrl}/companies`)
      .flush({ message: 'Invalid or expired token.' }, { status: 401, statusText: 'Unauthorized' });

    expect(logoutSpy).toHaveBeenCalled();
    expect(observedError).toBeTruthy();
  });
});
