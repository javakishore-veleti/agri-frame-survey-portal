import { TestBed } from '@angular/core/testing';

import { AnalyticsApi } from './analytics-api';

describe('AnalyticsApi', () => {
  let service: AnalyticsApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AnalyticsApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
