// nav.tokens.ts
import { APP_INITIALIZER, Provider } from '@angular/core';
import { NavItem } from './nav.types';
import { NavRegistry } from './nav.registry';

export function provideRootNav(items: NavItem[]): Provider {
  return {
    provide: APP_INITIALIZER,
    multi: true,
    deps: [NavRegistry],
    useFactory: (reg: NavRegistry) => () => reg.register(items)
  };
}
