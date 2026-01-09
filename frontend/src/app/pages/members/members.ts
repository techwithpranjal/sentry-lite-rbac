import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

import { AuthService } from '../../services/auth.service';
import { MembersService } from '../../services/members.service';

@Component({
  standalone: true,
  selector: 'app-members',
  imports: [CommonModule],
  templateUrl: './members.html',
})

export class MembersComponent implements OnInit {
  appId!: number;
  roleId!: number;

  members: any[] = [];
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService,
    private membersService: MembersService
  ) {}

  ngOnInit() {
    this.appId = Number(this.route.snapshot.paramMap.get('appId'));
    this.roleId = Number(this.route.snapshot.paramMap.get('roleId'));

    this.checkAccess();
  }

  checkAccess() {
    this.authService.getIdentity().subscribe({
      next: (identity) => {
        const isOwner = identity.owned_apps.some(
          (app: any) => app.id === this.appId
        );
  
        const isMember = identity.memberships.some(
          (m: any) => m.role_id === this.roleId
        );
  
        if (!isOwner && !isMember) {
          this.router.navigate(['/roles', this.appId]);
          return;
        }
  
        this.loadMembers();
      },
      error: () => {
        this.router.navigate(['/roles', this.appId]);
      },
    });
  }

  loadMembers() {
    this.membersService.getMembersByRole(this.roleId).subscribe({
      next: (res: any[]) => {
        this.members = res;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

}