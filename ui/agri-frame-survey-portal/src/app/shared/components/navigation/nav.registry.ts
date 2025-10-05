import { Injectable, computed, signal } from '@angular/core';
import { NavItem } from './nav.types';

@Injectable({ providedIn: 'root' })
export class NavRegistry {
  private _items = signal<NavItem[]>([]);
  readonly items = computed(() => this._items());

  register(items: NavItem[]) {
    this._items.update(curr => [...curr, ...items]);
  }
}
