import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { CurrentUserResponseDTO, LoginRequestDTO, LoginResponseDTO } from './auth.models';

const TOKEN_KEY = 'aisdr_access_token';
const USER_KEY = 'aisdr_current_user';

/** No refresh-token flow (v1 design decision, see PARK-F-AUTH) -- when
 * the access token expires the interceptor's 401 handling logs the user
 * out and they log back in. Token + user are both cached in localStorage
 * so a page refresh doesn't need an extra /auth/me round trip just to
 * repopulate the signal. */
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly base = `${environment.apiBaseUrl}/auth`;

  private readonly _currentUser = signal<CurrentUserResponseDTO | null>(this.readStoredUser());
  readonly currentUser = this._currentUser.asReadonly();
  readonly isAuthenticated = computed(() => this._currentUser() !== null);

  login(dto: LoginRequestDTO): Observable<LoginResponseDTO> {
    return this.http.post<LoginResponseDTO>(`${this.base}/login`, dto).pipe(
      tap((response) => {
        localStorage.setItem(TOKEN_KEY, response.access_token);
        localStorage.setItem(USER_KEY, JSON.stringify(response.user));
        this._currentUser.set(response.user);
      }),
    );
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this._currentUser.set(null);
    this.router.navigateByUrl('/login');
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  private readStoredUser(): CurrentUserResponseDTO | null {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as CurrentUserResponseDTO;
    } catch {
      return null;
    }
  }
}
