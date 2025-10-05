import { NgModule, APP_INITIALIZER } from '@angular/core';
import { AdminRoutingModule } from './admin-routing-module';
import { NavRegistry } from '@shared/components/navigation/nav.registry';

@NgModule({
  imports: [AdminRoutingModule],
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
export class AdminModule { /* no constructor here */ }
