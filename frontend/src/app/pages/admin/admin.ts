import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../services/admin.service';

@Component({
  standalone: true,
  selector: 'app-admin',
  imports: [CommonModule],
  templateUrl: './admin.html',
})
export class AdminComponent implements OnInit {
  activeTab: 'overview' | 'apps' | 'roles' | 'requests' | 'memberships' = 'overview';

  stats: any = null;
  pendingRequests: any[] = [];
  apps : any[] = [];
  roles : any[] = [];
  memberships : any[] = [];
  requests : any[] = [];

  loading = false;

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.loadOverview();
  }

  setTab(tab: any) {
    this.activeTab = tab;

    switch (tab) {
      case 'overview':
        this.loadOverview();
        break;
      case 'apps':
        this.loadApps();
        break;
      case 'roles':
        this.loadRoles();
        break;
      case 'requests':
        this.loadRequests();
        break;
      case 'memberships':
        this.loadMemberships();
        break;
    }
  }

  loadOverview() {
    this.loading = true;

    this.adminService.getOverview().subscribe({
      next: (res) => {
        this.stats = res.stats;
        this.pendingRequests = res.pending_requests;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  loadApps() {
    this.loading = true;

    this.adminService.getAdminApps().subscribe({
      next: (res) => {
        this.apps = res;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  loadRoles() {
    this.loading = true;

    this.adminService.getAdminRoles().subscribe({
      next: (res) => {
        this.roles = res;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  loadRequests() {
    this.loading = true;

    this.adminService.getAdminRequests().subscribe({
      next: (res) => {
        this.requests = res;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  loadMemberships() {
    this.loading = true;

    this.adminService.getAdminMemberships().subscribe({
      next: (res) => {
        this.memberships = res;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

}