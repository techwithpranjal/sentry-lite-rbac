import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MembersService {
  constructor(private http: HttpClient) {}

  getMembersByRole(roleId: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${environment.apiBaseUrl}/roles?app_id=${roleId}`,
      {
        headers: new HttpHeaders({
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        }),
      }
    );
  }
}