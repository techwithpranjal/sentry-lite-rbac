import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { AppsComponent } from './pages/apps/apps';
import { RolesComponent } from './pages/roles/roles';
import { AuthenticatedLayoutComponent } from './layouts/authenticated-layout/authenticated-layout';
import { authGuard } from './guards/auth.guard';
import { RegisterComponent } from './pages/register/register';
import { MembersComponent } from './pages/members/members';
import { AccessComponent } from './pages/access/access';
import { AdminComponent } from './pages/admin/admin';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: '',
    component: AuthenticatedLayoutComponent,
    canActivateChild: [authGuard],
    children: [
      { path: 'dashboard', component: DashboardComponent },
      { path: 'apps', component: AppsComponent },
      { path: 'roles', component: RolesComponent },
      { path: 'roles/:appId', component: RolesComponent },
      { path: 'roles/:appId/members/:roleId', component: MembersComponent },
      { path: 'access', component: AccessComponent },
      { path: 'admin', component: AdminComponent },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },

  // Fallback
  { path: '**', redirectTo: 'login' },
];
