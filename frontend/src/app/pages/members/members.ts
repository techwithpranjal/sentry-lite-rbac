import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

import { AuthService } from '../../services/auth.service';
import { MembersService } from '../../services/members.service';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-members',
  imports: [CommonModule, FormsModule],
  templateUrl: './members.html',
})
export class MembersComponent implements OnInit {
  appId!: number;
  roleId!: number;

  members: any[] = [];
  loading = true;

  isOwner = false;
  showAddModal = false;

  newMemberEmail = '';
  adding = false;

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
        const isOwner = identity.owned_apps.some((app: any) => app.id === this.appId);

        const isMember = identity.memberships.some((m: any) => m.role_id === this.roleId);

        if (!isOwner && !isMember) {
          this.router.navigate(['/roles', this.appId]);
          return;
        }

        this.isOwner = isOwner;
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

  closeAddMember() {
    this.showAddModal = false;
    this.newMemberEmail = '';
  }

  addMember() {
    if (!this.newMemberEmail) return;

    this.adding = true;

    this.membersService
      .addMember({
        user_email: this.newMemberEmail,
        app_id: this.appId,
        role_id: this.roleId,
      })
      .subscribe({
        next: () => {
          this.adding = false;
          this.closeAddMember();
          this.loadMembers();
        },
        error: () => {
          this.adding = false;
        },
      });
  }

  removeMember(membershipId: number) {
    if (!confirm('Remove this member from the role?')) return;
  
    this.membersService.deleteMember(membershipId).subscribe({
      next: () => this.loadMembers(),
    });
  }
}
