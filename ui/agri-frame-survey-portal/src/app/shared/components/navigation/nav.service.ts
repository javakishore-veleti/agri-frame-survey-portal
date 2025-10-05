import { Injectable, computed, inject } from '@angular/core';
import { NavRegistry } from './nav.registry';
import { AuthService } from '@core/services/auth.service';
import { FeatureFlagsService } from '@core/services/feature-flags.service';

@Injectable({ providedIn: 'root' })
export class NavService {
  private reg = inject(NavRegistry);
  private auth = inject(AuthService);
  private flags = inject(FeatureFlagsService);

  items = computed(() =>
    this.reg.items().map(i => ({
      ...i,
      children: i.children?.filter(c => this.auth.has(c.requiredPermission) && this.flags.isOn(c.featureFlag))
    }))
    .filter(i => this.auth.has(i.requiredPermission) && this.flags.isOn(i.featureFlag))
  );
}
