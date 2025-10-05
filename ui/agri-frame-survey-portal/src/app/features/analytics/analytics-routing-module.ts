import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard';

const routes: Routes = [{ path: '', component: DashboardComponent, title: 'Analytics' }];

@NgModule({ imports: [RouterModule.forChild(routes)], exports: [RouterModule] })
export class AnalyticsRoutingModule {}
