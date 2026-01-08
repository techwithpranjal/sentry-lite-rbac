import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { AppsComponent } from './pages/apps/apps';
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
      // { path: 'requests', loadComponent: () => import('./pages/requests/requests').then(m => m.RequestsComponent) },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },

  // Fallback
  { path: '**', redirectTo: 'dashboard' },
];