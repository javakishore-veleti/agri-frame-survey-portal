export interface SurveySummary {
  id: string;
  name: string;
  status: 'Draft' | 'Active' | 'Closed';
  updatedAt: string;
}
