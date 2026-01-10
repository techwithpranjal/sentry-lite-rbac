import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiBaseUrl;
  private TOKEN_KEY = 'access_token';
  private _isAdmin = false;

  constructor(private http: HttpClient) {}

  login(payload: { email: string; password: string }) {
    return this.http.post<any>(`${this.apiUrl}/auth/login`, payload).pipe(
      tap((res) => {
        if (res?.access_token) {
          localStorage.setItem(this.TOKEN_KEY, res.access_token);
        }
      })
    );
  }

  register(email: string, password: string) {
    return this.http.post(`${environment.apiBaseUrl}/auth/register`, { email, password });
  }

  getToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getIdentity() {
    return this.http
      .get<any>(`${this.apiUrl}/auth/identity`, {
        headers: {
          Authorization: `Bearer ${this.getToken()}`,
        },
      })
      .pipe(
        tap((res) => {
          this._isAdmin = !!res.user?.is_admin;
        })
      );
  }

  isAdmin() {
    return this._isAdmin;
  }
}
