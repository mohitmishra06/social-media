import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OtpValidator } from './otp-validator';

describe('OtpValidator', () => {
  let component: OtpValidator;
  let fixture: ComponentFixture<OtpValidator>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OtpValidator]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OtpValidator);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
