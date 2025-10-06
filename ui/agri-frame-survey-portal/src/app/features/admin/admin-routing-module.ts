import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UsersComponent } from './pages/users/users';
import { RolesComponent } from './pages/roles/roles';
import { TenantsComponent } from './pages/tenants/tenants';
import {AboutUsersComponent} from '@features/admin/pages/users/about-users/about-users';

const routes: Routes = [
  { path: '', redirectTo: 'users', pathMatch: 'full' },
  { path: 'about-users', component: AboutUsersComponent, title: 'Admin - About Users' },
  { path: 'users', component: UsersComponent, title: 'Admin - Users' },
  { path: 'roles', component: RolesComponent, title: 'Admin - Roles' },
  { path: 'tenants', component: TenantsComponent, title: 'Admin - Tenants' },
];

@NgModule({ imports: [RouterModule.forChild(routes)], exports: [RouterModule] })
export class AdminRoutingModule {}
