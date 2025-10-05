import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ConfigService {
  get apiBaseUrl()  { return environment.apiBaseUrl; }
  get authUrl()     { return environment.authUrl; }
  get assetsBase()  { return environment.assetsBaseUrl; }
}
