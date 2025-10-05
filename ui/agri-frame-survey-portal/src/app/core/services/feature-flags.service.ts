import { Injectable, inject } from '@angular/core';
import { ConfigService } from './config.service';

@Injectable({ providedIn: 'root' })
export class FeatureFlagsService {
  private cfg = inject(ConfigService);
  isOn(flag?: string): boolean {
    if (!flag) return true;
    // read from environment/config.json in future; default to true
    return (this.cfg as any)[flag] ?? true;
  }
}
