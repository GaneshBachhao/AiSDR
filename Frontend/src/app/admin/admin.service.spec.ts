import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { AdminService } from './admin.service';
import { AIConfigDiagnosticsResponse } from './admin.models';

describe('AdminService', () => {
  let service: AdminService;
  let httpMock: HttpTestingController;

  const sample: AIConfigDiagnosticsResponse = {
    default_provider: 'gemini',
    fallback_order: [],
    providers: [
      {
        provider: 'gemini',
        configured: true,
        model: 'gemini-3.5-flash',
        key_fingerprint: '***Ot5A',
        key_source: 'dotenv_file',
      },
    ],
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(AdminService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('fetches the effective AI provider config', () => {
    service.getAiConfig().subscribe();
    const req = httpMock.expectOne(`${environment.apiBaseUrl}/admin/ai-config`);
    expect(req.request.method).toBe('GET');
    req.flush(sample);
  });
});
