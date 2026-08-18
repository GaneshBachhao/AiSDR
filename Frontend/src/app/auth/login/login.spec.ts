import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { vi } from 'vitest';
import { environment } from '../../../environments/environment';
import { Login } from './login';

describe('Login', () => {
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Login],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('renders email and password fields and a submit control', () => {
    const fixture = TestBed.createComponent(Login);
    fixture.detectChanges();

    const el = fixture.nativeElement;
    expect(el.querySelector('input[name="email"]')).toBeTruthy();
    expect(el.querySelector('input[name="password"]')).toBeTruthy();
    expect(el.querySelector('button[type="submit"]')).toBeTruthy();
  });

  it('submitting valid credentials navigates away on success', async () => {
    const fixture = TestBed.createComponent(Login);
    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    fixture.detectChanges();

    const component = fixture.componentInstance;
    component['email'].set('jane@example.com');
    component['password'].set('correct-password');
    component.submit();

    httpMock.expectOne(`${environment.apiBaseUrl}/auth/login`).flush({
      access_token: 'a-real-looking-jwt',
      token_type: 'bearer',
      expires_in: 28800,
      user: { id: 'u1', email: 'jane@example.com', is_active: true },
    });

    expect(navigateSpy).toHaveBeenCalledWith('/');
  });

  it('a 401 response renders a visible generic error and does not navigate', () => {
    const fixture = TestBed.createComponent(Login);
    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    fixture.detectChanges();

    const component = fixture.componentInstance;
    component['email'].set('jane@example.com');
    component['password'].set('wrong-password');
    component.submit();

    httpMock.expectOne(`${environment.apiBaseUrl}/auth/login`).flush(
      {
        success: false,
        message: 'Invalid email or password.',
        error_code: 'UNAUTHORIZED',
        details: {},
      },
      { status: 401, statusText: 'Unauthorized' },
    );
    fixture.detectChanges();

    const errorEl = fixture.nativeElement.querySelector('.error');
    expect(errorEl?.textContent).toContain('Invalid email or password.');
    expect(navigateSpy).not.toHaveBeenCalled();
  });
});
