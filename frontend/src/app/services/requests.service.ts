import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class RequestsService {
  
  private apiUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  createRequest(payload: {
    app_id: number;
    role_id: number;
    justification: string;
  }) {
    return this.http.post<any>(`${this.apiUrl}/requests`, payload, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      }
    });
  }
    
}