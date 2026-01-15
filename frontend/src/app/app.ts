import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthService } from './services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
})
export class App {
  constructor(public authService: AuthService) {
    if (this.authService.isAuthenticated()) {
      this.authService.getIdentity().subscribe();
    }
  }
}

