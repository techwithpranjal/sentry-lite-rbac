import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SideNav } from '../../components/side-nav/side-nav';

@Component({
  selector: 'app-authenticated-layout',
  standalone: true,
  imports: [RouterOutlet, SideNav],
  templateUrl: './authenticated-layout.html',
})
export class AuthenticatedLayoutComponent {}