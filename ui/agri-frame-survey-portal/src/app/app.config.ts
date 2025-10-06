import { ApplicationConfig, APP_INITIALIZER } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { NavRegistry } from '@shared/components/navigation/nav.registry';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    {
      provide: APP_INITIALIZER,
      multi: true,
      deps: [NavRegistry],
      useFactory: (reg: NavRegistry) => () => {
        reg.register([
          { label: 'Surveys',   path: '/surveys',   requiredPermission: 'surveys.read',   icon: 'bi-clipboard-check' },
          { label: 'Analytics', path: '/analytics', requiredPermission: 'analytics.read', icon: 'bi-graph-up' },
          {
            label: 'Admin', requiredPermission: 'admin.access', icon: 'bi-gear',
            children: [
              { label: 'Users',   path: '/admin/users',   requiredPermission: 'admin.users' },
              { label: 'About Users',   path: '/admin/about-users',   requiredPermission: 'admin.users' },
              { label: 'Roles',   path: '/admin/roles',   requiredPermission: 'admin.roles' },
              { label: 'Tenants', path: '/admin/tenants', requiredPermission: 'admin.tenants' }
            ]
          }
        ]);
      }
    }
  ],
};
