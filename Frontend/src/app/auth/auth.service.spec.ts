import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { vi } from 'vitest';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';
import { LoginResponseDTO } from './auth.models';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;
  const base = `${environment.apiBaseUrl}/auth`;

  const loginResponse: LoginResponseDTO = {
    access_token: 'a-real-looking-jwt',
    token_type: 'bearer',
    expires_in: 28800,
    user: { id: 'u1', email: 'jane@example.com', is_active: true },
  };

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('login posts to /auth/login and, on success, stores the token/user and becomes authenticated', () => {
    expect(service.isAuthenticated()).toBe(false);

    service.login({ email: 'jane@example.com', password: 'correct-password' }).subscribe();
    const req = httpMock.expectOne(`${base}/login`);
    expect(req.request.method).toBe('POST');
    req.flush(loginResponse);

    expect(service.isAuthenticated()).toBe(true);
    expect(service.currentUser()?.email).toBe('jane@example.com');
    expect(service.getToken()).toBe('a-real-looking-jwt');
  });

  it('login on a 401 does not set currentUser or isAuthenticated', () => {
    service.login({ email: 'jane@example.com', password: 'wrong' }).subscribe({ error: () => {} });
    const req = httpMock.expectOne(`${base}/login`);
    req.flush(
      { success: false, message: 'Invalid email or password.', error_code: 'UNAUTHORIZED', details: {} },
      { status: 401, statusText: 'Unauthorized' },
    );

    expect(service.isAuthenticated()).toBe(false);
    expect(service.currentUser()).toBeNull();
  });

  it('logout clears storage, resets state, and navigates to /login', () => {
    service.login({ email: 'jane@example.com', password: 'correct-password' }).subscribe();
    httpMock.expectOne(`${base}/login`).flush(loginResponse);
    expect(service.isAuthenticated()).toBe(true);

    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);

    service.logout();

    expect(service.isAuthenticated()).toBe(false);
    expect(service.currentUser()).toBeNull();
    expect(service.getToken()).toBeNull();
    expect(navigateSpy).toHaveBeenCalledWith('/login');
  });

});

describe('AuthService rehydration from a pre-existing session', () => {
  beforeEach(() => {
    localStorage.clear();
    localStorage.setItem('aisdr_access_token', 'stored-token');
    localStorage.setItem(
      'aisdr_current_user',
      JSON.stringify({ id: 'u2', email: 'stored@example.com', is_active: true }),
    );

    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
  });

  afterEach(() => {
    TestBed.inject(HttpTestingController).verify();
    localStorage.clear();
  });

  it('rehydrates isAuthenticated()/currentUser() without any network call', () => {
    const rehydrated = TestBed.inject(AuthService);

    expect(rehydrated.isAuthenticated()).toBe(true);
    expect(rehydrated.currentUser()?.email).toBe('stored@example.com');
  });
});
