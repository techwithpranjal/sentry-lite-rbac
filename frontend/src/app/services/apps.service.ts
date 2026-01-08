import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AppsService {
  
  private apiUrl = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  getAllApps() {
    return this.http.get<any[]>(`${this.apiUrl}/apps`);
  }

  createApp(payload: {
    name: string;
    slug: string;
    description?: string;
  }) {
    return this.http.post<any>(`${this.apiUrl}/apps`, payload, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      }
    });
  }
}