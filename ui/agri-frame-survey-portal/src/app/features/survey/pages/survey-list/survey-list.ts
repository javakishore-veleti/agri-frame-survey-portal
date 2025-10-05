import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SurveyApiService } from '@domains/survey/services/survey-api.service';
import { SurveySummary } from '@domains/survey/models/survey-summary.model';

@Component({
  selector: 'af-survey-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <h2 class="mb-3">Surveys</h2>
    <div *ngIf="loading()">Loading...</div>
    <ul class="list-group" *ngIf="!loading()">
      <li class="list-group-item d-flex justify-content-between align-items-center"
          *ngFor="let s of surveys()">
        <span>{{ s.name }}</span>
        <a class="btn btn-sm btn-outline-primary" [routerLink]="['/surveys', s.id]">Open</a>
      </li>
    </ul>
  `,
})
export class SurveyListComponent {
  private api = inject(SurveyApiService);
  surveys = signal<SurveySummary[]>([]);
  loading = signal(true);

  ngOnInit() {
    this.api.list().subscribe({
      next: data => { this.surveys.set(data); this.loading.set(false); },
      error: () => this.loading.set(false)
    });
  }
}
