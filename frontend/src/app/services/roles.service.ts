import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RolesService {
  constructor(private http: HttpClient) {}

  getRolesByApp(appId: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${environment.apiBaseUrl}/roles?app_id=${appId}`,
      {
        headers: new HttpHeaders({
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
        }),
      }
    );
  }

  createRole(payload: {
    app_id: number;
    name: string;
    description: string;
  }) {
    return this.http.post(
      `${environment.apiBaseUrl}/roles?app_id=${payload.app_id}`,
      {
        app_id: payload.app_id,
        name: payload.name,
        description: payload.description,
      },
      {
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem('access_token')}`,
        },
      }
    );
  }
}