import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppsService } from '../../services/apps.service';
import { AuthService } from '../../services/auth.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

type Tab = 'all' | 'owned';

@Component({
  standalone: true,
  selector: 'app-apps',
  imports: [CommonModule, FormsModule],
  templateUrl: './apps.html',
})
export class AppsComponent implements OnInit {
  activeTab: Tab = 'all';

  allApps: any[] = [];
  ownedApps: any[] = [];

  loading = true;
  error = false;

  showCreateModal = false;

  newApp = {
    name: '',
    slug: '',
    description: '',
  };

  constructor(
    private appsService: AppsService,
    private identityService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadApps();
  }

  setTab(tab: Tab) {
    this.activeTab = tab;
  }

  loadApps() {
    this.loading = true;

    this.appsService.getAllApps().subscribe({
      next: (apps) => {
        this.allApps = apps;
        this.loading = false;
      },
      error: () => {
        this.error = true;
        this.loading = false;
      },
    });

    this.identityService.getIdentity().subscribe({
      next: (identity: { owned_apps: never[] }) => {
        this.ownedApps = identity.owned_apps || [];
      },
    });
  }

  openCreateModal() {
    this.showCreateModal = true;
  }

  closeCreateModal() {
    this.showCreateModal = false;
    this.newApp = { name: '', slug: '', description: '' };
  }

  generateSlug(name: string): string {
    return name
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-');
  }

  submitCreateApp() {
    const name = this.newApp.name.trim();
    if (!name) return;

    const payload = {
      name,
      slug: this.generateSlug(name),
      description: this.newApp.description,
    };

    this.appsService.createApp(payload).subscribe({
      next: () => {
        this.identityService.getIdentity().subscribe({
          next: (identity) => {
            this.ownedApps = identity.owned_apps || [];
          },
        });
        this.appsService.getAllApps().subscribe({
          next: (apps) => {
            this.allApps = apps;
          },
        });

        this.closeCreateModal();
      },
      error: (err) => {
        console.error('Failed to create app', err);
      },
    });
  }

  viewRoles(appId: number) {
    this.router.navigate(['/roles', appId]);
  }
}
