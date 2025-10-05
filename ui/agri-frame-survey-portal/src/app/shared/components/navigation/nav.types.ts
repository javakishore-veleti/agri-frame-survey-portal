export interface NavItem {
  label: string;
  path?: string;                 // '/surveys'
  icon?: string;                 // 'bi-graph-up'
  requiredPermission?: string;   // 'surveys.read'
  children?: NavItem[];          // dropdowns
  featureFlag?: string;          // 'analytics.enabled'
}
