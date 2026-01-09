import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RequestsService {
  private apiUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  getMyRequests(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/requests/me`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
  }

  createRequest(payload: { app_id: number; role_id: number; justification: string }) {
    return this.http.post<any>(`${this.apiUrl}/requests`, payload, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
  }

  approveOrReject(requestId: number, status: 'approved' | 'rejected') {
    return this.http.post(
      `${this.apiUrl}/requests/${requestId}/update`,
      { request_id: requestId, status: status },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }
    );
  }

  getMyApprovals() {
    return this.http.get<any[]>(`${this.apiUrl}/requests/approvals`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
  }
}
