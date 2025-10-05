import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SurveyListComponent }   from './pages/survey-list/survey-list';
import { SurveyViewerComponent } from './pages/survey-viewer/survey-viewer';
import { SurveyEditorComponent } from './pages/survey-editor/survey-editor';

const routes: Routes = [
  { path: '', component: SurveyListComponent, title: 'Surveys' },
  { path: 'new', component: SurveyEditorComponent, title: 'New Survey' },
  { path: ':id', component: SurveyViewerComponent, title: 'Survey' },
  { path: ':id/edit', component: SurveyEditorComponent, title: 'Edit Survey' },
];

@NgModule({ imports: [RouterModule.forChild(routes)], exports: [RouterModule] })
export class SurveyRoutingModule {}
