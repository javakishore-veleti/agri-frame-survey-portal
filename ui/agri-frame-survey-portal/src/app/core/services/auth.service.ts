import { Injectable, signal } from '@angular/core';

export type Role = 'Planner' | 'Analyst' | 'Admin';
export interface User { id: string; name: string; roles: Role[]; permissions: string[]; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  // In real app, fill from Identity service/JWT claims:
  private _user = signal<User | null>(null);

  user = this._user.asReadonly();

  loginAsDemo(role: Role = 'Admin') {
    const permsByRole: Record<Role, string[]> = {
      Planner: ['surveys.read'],
      Analyst: ['analytics.read'],
      Admin:   ['surveys.read','analytics.read','admin.access','admin.users','admin.roles','admin.tenants']
    };
    this._user.set({ id: 'u1', name: 'Demo', roles: [role], permissions: permsByRole[role] });
  }

  logout() { this._user.set(null); }

  has(permission?: string): boolean {
    if (!permission) return true;
    const u = this._user();
    return !!u?.permissions.includes(permission);
  }
}
