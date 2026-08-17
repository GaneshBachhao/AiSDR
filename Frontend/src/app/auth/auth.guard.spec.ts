import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, UrlTree, provideRouter, convertToParamMap } from '@angular/router';
import { authGuard } from './auth.guard';
import { AuthService } from './auth.service';

describe('authGuard', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    });
  });

  afterEach(() => localStorage.clear());

  function runGuard(): boolean | UrlTree {
    return TestBed.runInInjectionContext(() =>
      authGuard(
        { paramMap: convertToParamMap({}) } as never,
        { url: '/companies' } as never,
      ),
    ) as boolean | UrlTree;
  }

  it('allows navigation when the user is authenticated', () => {
    localStorage.setItem('aisdr_access_token', 'stored-token');
    localStorage.setItem(
      'aisdr_current_user',
      JSON.stringify({ id: 'u1', email: 'jane@example.com', is_active: true }),
    );

    expect(runGuard()).toBe(true);
  });

  it('redirects to /login when the user is not authenticated', () => {
    const result = runGuard();

    expect(result).toBeInstanceOf(UrlTree);

    const router = TestBed.inject(Router);
    expect(router.serializeUrl(result as UrlTree)).toBe('/login');
  });
});
