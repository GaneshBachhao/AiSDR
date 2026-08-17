import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly email = signal('');
  protected readonly password = signal('');
  protected readonly submitting = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  submit(): void {
    this.submitting.set(true);
    this.errorMessage.set(null);

    this.authService.login({ email: this.email(), password: this.password() }).subscribe({
      next: () => this.router.navigateByUrl('/'),
      error: () => {
        // Deliberately generic, matching the backend's own anti-enumeration
        // stance -- never hint whether the email or the password was wrong.
        this.errorMessage.set('Invalid email or password.');
        this.submitting.set(false);
      },
    });
  }
}
