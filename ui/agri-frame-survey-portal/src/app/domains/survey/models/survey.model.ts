export interface Survey {
  id: string;
  name: string;
  description?: string;
  sections: Array<{ id: string; title: string; order: number }>;
  createdAt: string;
  updatedAt: string;
}
