import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { Admin } from './admin';
import { AIConfigDiagnosticsResponse } from './admin.models';

describe('Admin', () => {
  let httpMock: HttpTestingController;

  const config: AIConfigDiagnosticsResponse = {
    default_provider: 'gemini',
    fallback_order: ['gemini', 'openai'],
    providers: [
      {
        provider: 'gemini',
        configured: true,
        model: 'gemini-3.5-flash',
        key_fingerprint: '***Ot5A',
        key_source: 'dotenv_file',
      },
      {
        provider: 'azure_openai',
        configured: false,
        model: 'gpt-4.1',
        key_fingerprint: null,
        key_source: 'not_set',
      },
    ],
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Admin],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('renders the resolved provider config, including a masked fingerprint and an unconfigured provider', async () => {
    const fixture = TestBed.createComponent(Admin);
    fixture.detectChanges();

    httpMock.expectOne(`${environment.apiBaseUrl}/admin/ai-config`).flush(config);
    await fixture.whenStable();
    fixture.detectChanges();

    const text = fixture.nativeElement.textContent;
    expect(text).toContain('gemini');
    expect(text).toContain('gemini → openai');
    expect(text).toContain('***Ot5A');

    const rows = fixture.nativeElement.querySelectorAll('tbody tr');
    expect(rows.length).toBe(2);
    expect(rows[0].querySelector('.badge').classList).toContain('badge-ok');
    expect(rows[1].querySelector('.badge').classList).toContain('badge-neutral');
    expect(rows[1].textContent).toContain('not_set');
  });
});
