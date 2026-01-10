import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-side-nav',
  imports: [CommonModule, RouterModule],
  templateUrl: './side-nav.html',
  standalone: true,
})
export class SideNav {
  constructor(public authService: AuthService) {}
}
