import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { AIConfigDiagnosticsResponse } from './admin.models';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private readonly http = inject(HttpClient);

  getAiConfig(): Observable<AIConfigDiagnosticsResponse> {
    return this.http.get<AIConfigDiagnosticsResponse>(`${environment.apiBaseUrl}/admin/ai-config`);
  }
}
