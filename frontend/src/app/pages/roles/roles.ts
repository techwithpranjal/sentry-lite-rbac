import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ActivatedRoute, Router } from '@angular/router';
import { AppsService } from '../../services/apps.service';
import { RolesService } from '../../services/roles.service';
import { AuthService } from '../../services/auth.service';
import { RequestsService } from '../../services/requests.service';

@Component({
  standalone: true,
  selector: 'app-roles',
  imports: [CommonModule, FormsModule],
  templateUrl: './roles.html',
})
export class RolesComponent implements OnInit {
  apps: any[] = [];
  roles: any[] = [];
  memberships: number[] = [];

  selectedAppId: number | null = null;

  loading = false;

  showCreateModal = false;

  ownedApps: any[] = [];

  newRole = {
    app_id: 0,
    name: '',
    description: '',
  };

  showRequestModal = false;

  requestPayload = {
    app_id: 0,
    role_id: 0,
    justification: '',
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private appsService: AppsService,
    private rolesService: RolesService,
    private identityService: AuthService,
    private requestsService: RequestsService
  ) {}

  ngOnInit() {
    this.loadApps();

    this.route.paramMap.subscribe((params) => {
      this.selectedAppId = Number(params.get('appId'));
      if (this.selectedAppId) {
        this.loadRoles(this.selectedAppId);
      }
    });
  }

  loadApps() {
    this.appsService.getAllApps().subscribe({
      next: (apps) => (this.apps = apps),
    });
    this.identityService.getIdentity().subscribe((res) => {
      this.ownedApps = res.owned_apps;
      this.memberships = res.memberships.map((m: any) => m.role_id);
    });
  }

  onAppChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    const appId = select.value;

    if (!appId) return;

    this.router.navigate(['/roles', appId]);
  }

  loadRoles(appId: number) {
    this.loading = true;
    this.roles = [];

    this.rolesService.getRolesByApp(appId).subscribe({
      next: (res) => {
        this.roles = res;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  openCreateRole() {
    this.showCreateModal = true;
  }

  closeCreateRole() {
    this.showCreateModal = false;
    this.newRole = { app_id: 0, name: '', description: '' };
  }

  createRole() {
    if (!this.newRole.app_id || !this.newRole.name) return;

    const appId = this.newRole.app_id;

    this.rolesService.createRole(this.newRole).subscribe(() => {
      this.closeCreateRole();
      this.loadRoles(appId);

      this.router.navigate(['/roles', appId]);
    });
  }

  isMember(roleId: number): boolean {
    return this.memberships.includes(roleId);
  }

  isOwner(appId: number): boolean {
    return this.ownedApps.some((app) => app.id === appId);
  }

  canViewMembers(roleId: number): boolean {
    return this.isOwner(this.selectedAppId!) || this.isMember(roleId);
  }

  canRequestAccess(roleId: number): boolean {
    return !this.isMember(roleId);
  }

  viewMembers(roleId: number) {}

  openRequestAccess(roleId: number) {
    if (!this.selectedAppId) return;

    this.requestPayload = {
      app_id: this.selectedAppId,
      role_id: roleId,
      justification: '',
    };

    this.showRequestModal = true;
  }

  closeRequestAccess() {
    this.showRequestModal = false;
    this.requestPayload = { app_id: 0, role_id: 0, justification: '' };
  }

  submitRequestAccess() {
    if (!this.requestPayload.app_id || !this.requestPayload.role_id) return;

    this.requestsService.createRequest(this.requestPayload).subscribe({
      next: () => {
        this.closeRequestAccess();
      },
    });
  }
}
