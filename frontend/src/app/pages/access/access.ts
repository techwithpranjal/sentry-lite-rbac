import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RequestsService } from '../../services/requests.service';
import { AuthService } from '../../services/auth.service';

type AccessTab = 'requests' | 'approvals' | 'memberships';

@Component({
  standalone: true,
  selector: 'app-access',
  imports: [CommonModule],
  templateUrl: './access.html',
})
export class AccessComponent implements OnInit {
  activeTab: AccessTab = 'requests';

  loading = false;
  error = false;

  myRequests: any[] = [];
  myApprovals: any[] = [];
  myMemberships: any[] = [];

  constructor(private requestsService: RequestsService, private authService: AuthService) {}

  ngOnInit() {
    this.loadMyRequests();
  }

  setTab(tab: AccessTab) {
    this.activeTab = tab;
  
    if (tab === 'requests') this.loadMyRequests();
    if (tab === 'approvals') this.loadMyApprovals();
    if (tab === 'memberships') this.loadMyMemberships();
  }

  loadMyRequests() {
    this.loading = true;
    this.error = false;

    this.requestsService.getMyRequests().subscribe({
      next: (res) => {
        this.myRequests = res;
        this.loading = false;
      },
      error: () => {
        this.error = true;
        this.loading = false;
      },
    });
  }

  loadMyApprovals() {
    this.loading = true;
    this.error = false;

    this.requestsService.getMyApprovals().subscribe({
      next: (res) => {
        this.myApprovals = res.filter((req) => req.status === 'pending');
        this.loading = false;
      },
      error: () => {
        this.error = true;
        this.loading = false;
      },
    });
  }

  approve(requestId: number) {
    this.updateRequest(requestId, 'approved');
  }

  reject(requestId: number) {
    this.updateRequest(requestId, 'rejected');
  }

  private updateRequest(requestId: number, status: 'approved' | 'rejected') {
    this.requestsService.approveOrReject(requestId, status).subscribe(() => {
      this.loadMyApprovals();
    });
  }

  loadMyMemberships() {
    this.loading = true;
    this.error = false;

    this.authService.getIdentity().subscribe({
      next: (res) => {
        this.myMemberships = res.memberships || [];
        this.loading = false;
      },
      error: () => {
        this.error = true;
        this.loading = false;
      },
    });
  }
}
