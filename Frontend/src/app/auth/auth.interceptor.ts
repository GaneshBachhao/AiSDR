import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';

/** Attaches the bearer token to every request against this app's own
 * API, and logs the user out on a 401 (expired/invalid token) so a stale
 * session doesn't just keep failing silently. */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);

  const isApiRequest = req.url.startsWith(environment.apiBaseUrl);
  const isLoginRequest = req.url.startsWith(`${environment.apiBaseUrl}/auth/login`);
  const token = authService.getToken();

  const authedReq =
    isApiRequest && !isLoginRequest && token
      ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
      : req;

  return next(authedReq).pipe(
    catchError((err: HttpErrorResponse) => {
      if (isApiRequest && err.status === 401) {
        authService.logout();
      }
      return throwError(() => err);
    }),
  );
};
