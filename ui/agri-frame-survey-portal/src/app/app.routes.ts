import { Routes } from '@angular/router';


export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'surveys' },
  { path: 'surveys',   loadChildren: () => import('@features/survey/survey-module').then(m => m.SurveyModule) },
  { path: 'analytics', loadChildren: () => import('@features/analytics/analytics-module').then(m => m.AnalyticsModule) },
  { path: 'admin',     loadChildren: () => import('@features/admin/admin-module').then(m => m.AdminModule) },
  { path: '**', redirectTo: 'surveys' },
];
