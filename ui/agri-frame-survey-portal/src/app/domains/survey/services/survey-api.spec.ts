import { TestBed } from '@angular/core/testing';

import { SurveyApi } from './survey-api';

describe('SurveyApi', () => {
  let service: SurveyApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SurveyApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
