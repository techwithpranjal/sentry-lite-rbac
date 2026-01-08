import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { AppsComponent } from './pages/apps/apps';
import { RolesComponent } from './pages/roles/roles';
import { AuthenticatedLayoutComponent } from './layouts/authenticated-layout/authenticated-layout';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: AuthenticatedLayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: 'dashboard', component: DashboardComponent },
      { path: 'apps', component: AppsComponent },
      { path: 'roles', component: RolesComponent },
      { path: 'roles/:appId', component: RolesComponent },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },

  // Fallback
  { path: '**', redirectTo: 'dashboard' },
];
