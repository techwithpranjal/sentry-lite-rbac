import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private baseUrl = environment.apiBaseUrl + '/admin';

  constructor(private http: HttpClient) {}

  getOverview() {
    return this.http.get<any>(`${this.baseUrl}/overview`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
  }

  getAdminApps() {
    return this.http.get<any>(`${this.baseUrl}/apps`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
  }

  getAdminRoles() {
    return this.http.get<any>(`${this.baseUrl}/roles`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
  }

  getAdminRequests() {
    return this.http.get<any>(`${this.baseUrl}/requests`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
  }

  getAdminMemberships() {
    return this.http.get<any>(`${this.baseUrl}/memberships`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    });
  }
}