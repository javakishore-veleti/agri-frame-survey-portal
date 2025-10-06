import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AboutUsers } from './about-users';

describe('AboutUsers', () => {
  let component: AboutUsers;
  let fixture: ComponentFixture<AboutUsers>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AboutUsers]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AboutUsers);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
