import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
})
export class DashboardComponent implements OnInit {
  identity: any = null;
  loading = true;
  error = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.getIdentity().subscribe({
      next: (data) => {
        console.log('Identity data:', data);
        this.identity = data;
        this.loading = false;
      },
      error: () => {
        this.error = true;
        this.loading = false;
      },
    });
  }
}