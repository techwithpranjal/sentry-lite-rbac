import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MembersService {
  constructor(private http: HttpClient) {}

  getMembersByRole(roleId: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${environment.apiBaseUrl}/memberships?role_id=${roleId}`,
      {
        headers: new HttpHeaders({
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
        }),
      }
    );
  }

  addMember(payload: {
    user_email: string;
    app_id: number;
    role_id: number;
  }) {
    return this.http.post<any>(`${environment.apiBaseUrl}/memberships`, payload, {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
      }
    });
  }

  deleteMember(membershipId: number) {
    return this.http.delete<any>(`${environment.apiBaseUrl}/memberships?membership_id=${membershipId}`, {
      headers: {
        Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
      }
    });
  }
}