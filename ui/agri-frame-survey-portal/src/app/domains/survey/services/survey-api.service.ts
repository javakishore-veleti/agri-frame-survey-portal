import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from '@core/services/config.service';
import { Observable } from 'rxjs';
import { Survey } from '../models/survey.model';
import { SurveySummary } from '../models/survey-summary.model';

@Injectable({ providedIn: 'root' })
export class SurveyApiService {
  private http = inject(HttpClient);
  private cfg = inject(ConfigService);
  private base = this.cfg.apiBaseUrl;

  list(): Observable<SurveySummary[]> { return this.http.get<SurveySummary[]>(`${this.base}/surveys`); }
  get(id: string): Observable<Survey> { return this.http.get<Survey>(`${this.base}/surveys/${id}`); }
  create(dto: Partial<Survey>): Observable<Survey> { return this.http.post<Survey>(`${this.base}/surveys`, dto); }
  update(id: string, dto: Partial<Survey>): Observable<Survey> { return this.http.put<Survey>(`${this.base}/surveys/${id}`, dto); }
  delete(id: string): Observable<void> { return this.http.delete<void>(`${this.base}/surveys/${id}`); }
}
