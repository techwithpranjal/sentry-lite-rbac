import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ActivatedRoute, Router } from '@angular/router';
import { AppsService } from '../../services/apps.service';
import { RolesService } from '../../services/roles.service';
import { AuthService } from '../../services/auth.service';

@Component({
  standalone: true,
  selector: 'app-roles',
  imports: [CommonModule, FormsModule],
  templateUrl: './roles.html',
})
export class RolesComponent implements OnInit {
  apps: any[] = [];
  roles: any[] = [];

  selectedAppId: number | null = null;

  loading = false;

  showCreateModal = false;

  ownedApps: any[] = [];

  newRole = {
    app_id: 0,
    name: '',
    description: '',
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private appsService: AppsService,
    private rolesService: RolesService,
    private identityService: AuthService
  ) {}

  ngOnInit() {
    this.loadApps();

    this.route.paramMap.subscribe((params) => {
      this.selectedAppId = Number(params.get('appId'));
      console.log('Selected App ID:', this.selectedAppId);
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
}
