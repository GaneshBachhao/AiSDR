import { Component, OnInit, inject, signal } from '@angular/core';
import { AdminService } from './admin.service';
import { AIConfigDiagnosticsResponse } from './admin.models';

@Component({
  selector: 'app-admin',
  standalone: true,
  templateUrl: './admin.html',
  styleUrl: './admin.scss',
})
export class Admin implements OnInit {
  private readonly service = inject(AdminService);

  protected readonly config = signal<AIConfigDiagnosticsResponse | null>(null);
  protected readonly loading = signal(true);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.service.getAiConfig().subscribe({
      next: (config) => {
        this.config.set(config);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Could not load AI provider diagnostics. Check that the API is running.');
        this.loading.set(false);
      },
    });
  }
}
