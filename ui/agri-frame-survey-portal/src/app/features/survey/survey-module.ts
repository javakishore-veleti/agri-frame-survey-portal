import { NgModule, APP_INITIALIZER } from '@angular/core';
import { SurveyRoutingModule } from './survey-routing-module';
import { NavRegistry } from '@shared/components/navigation/nav.registry';

@NgModule({
  imports: [SurveyRoutingModule],
  providers: [
    {
      provide: APP_INITIALIZER,
      multi: true,
      deps: [NavRegistry],
      useFactory: (reg: NavRegistry) => () => {
        // contribute menu entries when this lazy module loads
        // (optional if you already seeded in app.config.ts)
        // reg.register([{ label: 'Audit', path: '/admin/audit', requiredPermission: 'admin.audit' }]);
      }
    }
  ]
})
export class SurveyModule { /* no constructor here */ }



